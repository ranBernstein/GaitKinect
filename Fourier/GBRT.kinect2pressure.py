import numpy as np
import angleExtraction
import sys
import RNN
from sklearn.metrics import mean_squared_error
from sklearn.datasets import make_friedman1
from sklearn.ensemble import GradientBoostingRegressor
from jointsMap import ancestorMap, Joints
from sets import Set
import matplotlib.pyplot as plt
from threading import Thread
from multiprocessing import Pool
from thresholdFinder import normalByPercentile

featureSpaceIndices = np.array([15, 19, 23, 27, 31, 35, 39, 43, 47, 51, 59, 63, 67, 75, 79, 83])
#featureSpaceIndices = np.array([51, 83])
fileName = 'inputs/asc_gyro_l.skl'
outFile = 'out.txt'
featureNum  = len(featureSpaceIndices)


def evalSensor(sensorIndex, featureSpaceIndices):
    #reset data structure
    allByTime = {}
    f = open(fileName, 'r')
    headers = f.readline().split()
    for line in f:
        splited = line.split() 
        timeStamp = int(splited[0])
        allByTime[timeStamp] = {}
    f.close()
    allByJoint = {}
    for inputIndices in featureSpaceIndices:
        allByJoint[inputIndices] = {}
    clfs = {}
    grades = {}
    for inputIndices in featureSpaceIndices:
        allByTime, allByJoint = angleExtraction.prepareAnglesFromInput(fileName, inputIndices, sensorIndex, True, allByTime, allByJoint)
    
    #normalizing  allByJoint
    timeSet = Set([])
    for inputIndices in featureSpaceIndices:
        vec = []
        for timeStamp in allByTime.keys():
            if(timeStamp in allByJoint[inputIndices].keys()):
                timeSet.add(timeStamp)
                x = allByJoint[inputIndices][timeStamp]
                vec.append(x)
        if(len(vec) > 0):
            vec = angleExtraction.normelizeVector(vec)
        i=0
        for timeStamp in  allByTime.keys():
            if(timeStamp in allByJoint[inputIndices].keys()):
                allByJoint[inputIndices][timeStamp] = vec[i]
                i = i + 1
    
    #time set to list, output dict to list 
    time = []
    for timeStamp in timeSet:
        time.append(timeStamp)
    time.sort()
    allOutput = []
    tmpTime = []
    #clean zeros, craete time ordered output vector
    for timeStamp in time:
        out = allByTime[timeStamp]['output']
        if(out != 0):
            tmpTime.append(timeStamp)
            allOutput.append(out)
    time = tmpTime 

    #normalize allOutput
    allOutput = normalByPercentile(allOutput)
    allOutputMap = {}
    i=0
    for timeStamp in time:
        allOutputMap[timeStamp] = allOutput[i]
        i = i + 1
    
    
    #training a clf for each joint
    for inputIndices in featureSpaceIndices:
        x=[]
        y=[]
        for timeStamp, angle in allByJoint[inputIndices].iteritems():
            if(timeStamp in allOutputMap.keys()):
                x.append(angle)
                y.append(allOutputMap[timeStamp])
        if(len(y) == 0):
            continue;
        gradeFactor, clf = getEstimationFactored(x, y)
        clfs[inputIndices] = clf
        grades[inputIndices] = gradeFactor 
         
    #classifying by all the clfs                
    trainSize = int(0.7*len(time))
    time_train, time_test = time[:trainSize], time[trainSize:]
    y_train, y_test =  allOutput[:trainSize], allOutput[trainSize:]
    expectedOutputMap = {}
    predictionMap = {}
    weights = {}
    for timeStamp in time_test:
        expectedOutputMap[timeStamp] = allOutputMap[timeStamp]
        for inputIndices in featureSpaceIndices:
            if(timeStamp in allByJoint[inputIndices].keys()):
                x = allByJoint[inputIndices][timeStamp]
                p = clfs[inputIndices].predict(x)
                if(p > 0):
                    y = 1
                else:
                    y=-1
                predictionMap[timeStamp] = predictionMap.get(timeStamp, 0) + y*grades[inputIndices]
                weights[timeStamp] = weights.get(timeStamp, 0) + grades[inputIndices]
    #normalizing by the weights             
    for timeStamp in predictionMap.keys():
        if(weights[timeStamp] != 0):
            predictionMap[timeStamp] = predictionMap[timeStamp] / weights[timeStamp] 
        else:
            predictionMap.pop(timeStamp)
    if(len(predictionMap) == 0):
        grade = 0
        out = open(outFile, 'a')
        res = str(featureSpaceIndices) + " " + str(grade) + '\n'
        out.write(res)
        out.close()
        return grade
    #converting the maps to corresponding lists   
    expectedOutput = []
    prediction = []
    #for timeStamp, value in predictionMap.items():
    time = []
    for timeStamp in time_test:
        if(timeStamp in predictionMap.keys()):
            time.append(timeStamp)
            prediction.append(predictionMap[timeStamp])
            expectedOutput.append(expectedOutputMap[timeStamp])
    """   
    plt.plot(time,expectedOutput, color='blue')
    plt.plot(time,prediction, color='green')
    plt.show()
    """
    var = np.var(np.array(allOutput))
    
    #grade = var / mean_squared_error(expectedOutput, prediction)
    hits = 0.0
    for i in range(len(prediction)):
        if(prediction[i]*expectedOutput[i] > 0):
            hits+=1
    grade = hits / float(len(prediction))
    out = open(outFile, 'a')
    res = str(featureSpaceIndices) + " " + str(grade) + '\n'
    out.write(res)
    out.close()
    #if(grade > best):
     #   best = grade
      #  print res
    return  grade
        
        
def splitData(x, y):
    x = np.reshape(np.array(x), (len(x), 1))
    y = np.array(y)
    numOfSamples = len(x)
    trainSize = int(0.7*numOfSamples)
    testSize = numOfSamples - trainSize
    x_train, x_test = x[:trainSize], x[trainSize:]
    y_train, y_test = y[:trainSize], y[trainSize:]
    return x_train, x_test, y_train, y_test

def getEstimation(x, y):
    x_train, x_test, y_train, y_test = splitData(x, y)
    clf = GradientBoostingRegressor(n_estimators=100, learning_rate=0.01, max_depth=2, random_state=0, loss='ls').fit(x_train, y_train)
    prediction = clf.predict(x_test)
    #clf, prediction = RNN.getPrediction(x_train, y_train, x_test)
    return prediction, y_test, clf
    
def  getEstimationFactored(x, y):
    prediction, y_test, clf = getEstimation(x, y)
    currOutputVar = np.var(np.array(y_test))
    hits = 0.0
    for i in range(len(prediction)):
        if(prediction[i]*y_test[i] > 0):
            hits+=1
    gradeFactor = hits / float(len(prediction)) - 0.5
    if(gradeFactor < 0):
        gradeFactor = 0
    return gradeFactor, clf
    
def bitfield(n):
    return np.array([1 if digit=='1' else 0 for digit in bin(n)[2:]])

out = open(outFile, 'wb')
out.flush()
out.close()
for n in xrange(1,2**featureNum):
    z = np.zeros((1, featureNum-len(bitfield(n))), dtype=int)
    chosen = np.append(z, bitfield(n))
    evalSensor(3, featureSpaceIndices[chosen.astype(np.bool)])
print 'end!' 
"""
if __name__ == '__main__':
    p = Pool(20)
    m={}
    out = open(outFile, 'wb')
    out.flush()
    out.close()
    best = 0
    for n in xrange(1,2**featureNum):
        z = np.zeros((1, featureNum-len(bitfield(n))), dtype=int)
        chosen = np.append(z, bitfield(n))
        if(n==3):
            pass
        m[n] = p.apply_async(evalSensor, [2, featureSpaceIndices[chosen.astype(np.bool)]])  
    for n in xrange(1,2**featureNum):
        z = np.zeros((1, featureNum-len(bitfield(n))), dtype=int)
        chosen = np.append(z, bitfield(n))
        try:
            res = m[n].get()
            if(res > best):
                best = res
                print str(featureSpaceIndices[chosen.astype(np.bool)]), str(res)
        except:
            print str(featureSpaceIndices[chosen.astype(np.bool)]), sys.exc_info()[0]
            pass
            
    print 'end!'      
 """   
    
    
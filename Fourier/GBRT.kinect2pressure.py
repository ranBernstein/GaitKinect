import numpy as np
import angleExtraction
from sklearn.metrics import mean_squared_error
from sklearn.datasets import make_friedman1
from sklearn.ensemble import GradientBoostingRegressor
from jointsMap import ancestorMap, Joints
from sets import Set
import matplotlib.pyplot as plt

featureSpaceIndices = [15, 19, 23, 27, 31, 35, 39, 43, 47, 51, 59, 63, 67, 75, 79, 83]
fileName = 'asc_gyro_l.skl'

def evalSensor(sensorIndex, featureSpaceIndices):
    #reset data structure
    allByTime = {}
    f = open(fileName, 'r')
    headers = f.readline().split()
    for line in f:
        splited = line.split() 
        timeStamp = int(splited[0])
        allByTime[timeStamp] = {}
    allByJoint = {}
    for inputIndices in featureSpaceIndices:
        allByJoint[inputIndices] = {}
    clfs = {}
    grades = {}
    for inputIndices in featureSpaceIndices:
        #print "sensor " + str(sensorIndex) + ", joint: " + str(inputIndices)
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
    allOutput = []
    for timeStamp in timeSet:
        time.append(timeStamp)
        
    time.sort()
    tmpTime = []
    tmpOut = []
    for timeStamp in time:
        allOutput.append(allByTime[timeStamp]['output'])
        if(63 in allByTime[timeStamp].keys()):
            tmpOut.append(allByTime[timeStamp][63])
            tmpTime.append(timeStamp)
    plt.plot(tmpTime, tmpOut, color='blue')
    #plt.plot(time_test,expectedOutput, color='green')
    plt.show()
    
    #normalize allOutput
    allOutput = angleExtraction.normelizeVector(allOutput)
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
                y = clfs[inputIndices].predict(x)
                predictionMap[timeStamp] = predictionMap.get(timeStamp, 0) + y*grades[inputIndices]
                weights[timeStamp] = weights.get(timeStamp, 0) + grades[inputIndices]
    #normalizing by the weights             
    for timeStamp in time_test:
        predictionMap[timeStamp] = predictionMap[timeStamp] / weights[timeStamp] 
    
    #converting the maps to corresponding lists   
    expectedOutput = []
    prediction = []
    for timeStamp, value in predictionMap.items():
        prediction.append(value)
        expectedOutput.append(expectedOutputMap[timeStamp])
        
    var = np.var(np.array(allOutput))
    
    return var / mean_squared_error(expectedOutput, prediction) 
        
        
def splitData(x, y):
    #y = angleExtraction.normelizeVector(y)
    #x = angleExtraction.normelizeInput(x)
    x = np.array(x)
    diam = len(np.shape(x))
    if(diam == 1):
        x = np.reshape(x, (len(x), 1))
    numOfSamples, numOfFeatures = np.shape(x)
    trainSize = int(0.7*numOfSamples)
    testSize = numOfSamples - trainSize
    x_train, x_test = x[:trainSize], x[trainSize:]
    y_train, y_test = y[:trainSize], y[trainSize:]
    return x_train, x_test, y_train, y_test

def getEstimation(x, y):
    x_train, x_test, y_train, y_test = splitData(x, y)
    clf = GradientBoostingRegressor(n_estimators=100, learning_rate=0.01, max_depth=1, random_state=0, loss='ls').fit(x_train, y_train)
    prediction = clf.predict(x_test)
    return prediction, y_test, clf
    
def  getEstimationFactored(x, y):
    prediction, y_test, clf = getEstimation(x, y)
    currOutputVar = np.var(np.array(y_test))
    mse = mean_squared_error(y_test, prediction)
    gradeFactor = mse/currOutputVar - 1
    return gradeFactor, clf
    
    
print evalSensor(2, featureSpaceIndices)    
    
    
    
    
    
    
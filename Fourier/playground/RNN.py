from pybrain.structure import LinearLayer, SigmoidLayer
from pybrain.structure import FullConnection
from pybrain.structure import RecurrentNetwork
from pybrain.tools.shortcuts import buildNetwork
from pybrain.supervised.trainers import BackpropTrainer
from pybrain.datasets import SequentialDataSet
from pybrain.structure import LSTMLayer

import numpy as np
import angleExtraction
import sys
from sets import Set
import matplotlib.pyplot as plt
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
    #clean zeros, create time ordered output vector
    for timeStamp in time:
        out = allByTime[timeStamp]['output']
        if(out != 0 and len(allByTime[timeStamp]) == featureNum + 1):
            tmpTime.append(timeStamp)
            allOutput.append(out)
    time = tmpTime 

    #normalize allOutput
    allOutput = normalByPercentile(allOutput)
    #create a net
    hiddenSize = (featureNum + 2)/2
    net = buildNetwork(featureNum, hiddenSize, 1, hiddenclass=LSTMLayer, outclass=SigmoidLayer, recurrent=True, bias=True) 
    #build dataset
    ds = SequentialDataSet(featureNum, 1)
    i=0
    lastTimeStamp = time[0]
    for timeStamp in time:
        if(len(allByTime[timeStamp]) == featureNum+1):#it is a full vector
            if(timeStamp - lastTimeStamp > 100):
                ds.newSequence()
            sample = []
            for inputIndices in featureSpaceIndices:
                sample.append(allByTime[timeStamp][inputIndices])
            ds.appendLinked(sample, allOutput[i])
        i = i + 1
        lastTimeStamp = timeStamp
    #train
    net.randomize()
    tstdata, trndata = ds.splitWithProportion( 0.25 )
    trainer = BackpropTrainer(net, trndata)
    print len(ds)
    min = 100
    trainNum = 100
    bestTrainer = None
    for i in range(trainNum):
        res = trainer.train()
        if(res < min):
            min = res
            bestTrainer = trainer
        net.randomize()
    print min
    """
    res = 100
    while(res > min):
        net.randomize()
        res = trainer.train()
    """
    trainer = bestTrainer
    for i in range(trainNum):
        res = trainer.train()
        if(i % (trainNum/10) == 0):
            print res
    print 'trndata.evaluateModuleMSE ' + str(trndata.evaluateModuleMSE(net))
    print 'tstdata.evaluateModuleMSE ' + str(tstdata.evaluateModuleMSE(net))
    #print net.activateOnDataset(tstdata)
    hits = 0.0
    total = 0.0
    #res = net.activate(tstdata)
    for i in range(trndata.getNumSequences()):
        for input, target in trndata.getSequenceIterator(i):
            res = net.activate(input)
            total += 1
            if(res[0]*target[0] > 0):
                hits+=1        
    grade = hits / total
    print 'grade ' + str(grade)
    print 'total ' + str(total)
def bitfield(n):
    return np.array([1 if digit=='1' else 0 for digit in bin(n)[2:]])


evalSensor(3, featureSpaceIndices)

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
    
    
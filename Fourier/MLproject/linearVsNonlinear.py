from pybrain.structure import FeedForwardNetwork
from pybrain.structure import LinearLayer, SigmoidLayer
from pybrain.structure import FullConnection
from pybrain.datasets import SupervisedDataSet
from pybrain.supervised.trainers import BackpropTrainer
from pybrain.structure.modules import BiasUnit
from pybrain.tools.neuralnets import NNregression
from pybrain.tools.shortcuts import buildNetwork
import math
import numpy as np
import matplotlib.pyplot as plt

def printError(n, ds, label, outputMax, outputMin):
    sum = 0
    for input, output in ds:
        pred = n.activate(input)
        sum+= (output - pred)**2
        #print input, pred
    rmse = math.sqrt(sum/len(ds))
    dif = outputMax - outputMin
    print rmse, dif
    print label, ' MSE: ', rmse/dif
    return rmse/dif

N = 5

def createDs(func):
    outputMax = -np.inf
    outputMin = np.inf
    global outputMax
    global outputMin
    ds = SupervisedDataSet( 2, 1 )
    for j in range(N):
        for i in range(N):
            input = [i,j]
            output = func(j, i)#math.sqrt(i**2+j**2)
            ds.appendLinked(input ,  output)
            if output > outputMax:
                outputMax = output
            if outputMin > output:
                outputMin = output
    ds.outputMax = outputMax
    ds.outputMin = outputMin
    return ds

def nonLinearFunc(i, j):
    return math.sqrt(i**2+j**2)
dsNonLinear = createDs(nonLinearFunc)     
dsNonLinear.label = 'non linear'
def linearFunc(i, j):
    return 2*i + 3*j
dsLinear = createDs(linearFunc)
dsLinear.label = 'linear'

epochsNum = 40
def evalFunc(ds):
    trains = []
    tests = []
    epochsNums = []
    parameters = range(1, 40)
    testAmount = 10
    for i in parameters:
        trainError = 0
        testError = 0
        for testNum in range(testAmount):
            tstdata, trndata = ds.splitWithProportion( 0.25 )
            hidden_size = i
            numOfEpocs = 10
            """
            n = buildNetwork( 1, hidden_size, 1, bias = True )
            
            
            """
            
            inLayer = LinearLayer(len(ds.getSample(0)[0]))
            hiddenLayer = SigmoidLayer(hidden_size)
            outLayer = LinearLayer(len(ds.getSample(0)[1]))
            n = FeedForwardNetwork()
            n.addInputModule(inLayer)
            n.addModule(hiddenLayer)
            b = BiasUnit()
            n.addModule(b)
            n.addOutputModule(outLayer)
            in_to_hidden = FullConnection(inLayer, hiddenLayer)
            hidden_to_out = FullConnection(hiddenLayer, outLayer)
            b_to_hidden = FullConnection(b, hiddenLayer)
            b_to_out = FullConnection(b, outLayer)
            
            n.addConnection(in_to_hidden)
            n.addConnection(hidden_to_out)
            n.addConnection(b_to_hidden)
            n.addConnection(b_to_out)
            
            n.sortModules()
            #print n.activate([1, 2])
            
            
            
            trainer = BackpropTrainer(n, trndata)#, verbose=True, weightdecay=0)
            trainer.trainUntilConvergence( verbose = True, validationProportion = 0.15, maxEpochs = epochsNum, continueEpochs = 10 )
            trainError += printError(n, trndata, 'trndata',ds.outputMax, ds.outputMin)
            testError += printError(n, tstdata, 'tstdata',ds.outputMax, ds.outputMin)
            epochsNums.append(epochsNum)
            #print n.activateOnDataset(tstdata)
        trains.append(trainError/testAmount)
        tests.append(testError/testAmount)
    
    plt.plot(parameters, trains, label='train '+ds.label)
    plt.plot(parameters, tests, label='test '+ds.label)
    plt.legend().draggable()
    plt.title('Hidden layer size influance ('+str(epochsNum)+' epochs)')
    plt.xlabel('Hidden layer size')
    plt.ylabel('Normalized RMSE')
    plt.grid()
evalFunc(dsNonLinear)
evalFunc(dsLinear)
plt.show()
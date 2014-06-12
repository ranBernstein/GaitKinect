from pybrain.structure import FeedForwardNetwork
from pybrain.structure import LinearLayer, SigmoidLayer
from pybrain.structure import FullConnection
from pybrain.datasets import SupervisedDataSet
from pybrain.supervised.trainers import BackpropTrainer
from pybrain.structure.modules import BiasUnit
from pybrain.tools.neuralnets import NNregression
from pybrain.tools.shortcuts import buildNetwork
import random
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

N = 1000
def nonLinearFunc(r):
    return math.sin(10*r)

def createDs(func):
    outputMax = -np.inf
    outputMin = np.inf
    global outputMax
    global outputMin
    ds = SupervisedDataSet( 1, 1 )
    #for j in range(N):
    rs = []
    for i in range(N):
        rs.append(random.random())
    rs.sort()
    for r in rs:
        input = r#[i]
        output = nonLinearFunc(r)
        ds.appendLinked(input ,  output)
        if output > outputMax:
            outputMax = output
        if outputMin > output:
            outputMin = output
    ds.outputMax = outputMax
    ds.outputMin = outputMin
    return ds

dsNonLinear = createDs(nonLinearFunc)     
dsNonLinear.label = 'non linear'

epochsNum = 100
def evalFunc(ds):
    trains = []
    tests = []
    epochsNums = []
    parameters = range(1, 40)
    testAmount = 10
    #for testNum in range(testAmount):
    tstdata, trndata = ds.splitWithProportion( 0.2 )
    hidden_size = 6
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
    
    
    initialLearningrate=1
    decay= 0.999995
    trainer = BackpropTrainer(n, trndata,  learningrate=initialLearningrate,\
                                lrdecay=decay, verbose=True, weightdecay=0)
    #trainer.trainUntilConvergence( verbose = True, validationProportion = 0.15, \
    #maxEpochs = epochsNum, continueEpochs = 10 )
    #print n.activateOnDataset(tstdata)
    first  = True
    num=4
    colors = plt.cm.jet(np.linspace(0, 1, num))
    for i in range(num):
        a=100
        trainer.trainEpochs(a)
        approx = []
        inputs = []
        reference = []
        sum =0
        for input, output in tstdata:
            res = n.activate(input)
            approx.append(res[0])
            inputs.append(input[0])
            reference.append(output[0])
            sum+=(res-output)**2
        rmse =math.sqrt(sum/len(tstdata))   
        if first:
            first = False
            plt.plot(inputs, reference, label='Original func')
        plt.scatter(inputs, approx, label=str((i+1)*a) + ' epochs, RMSE: '\
                    +str(rmse), c=colors[i])
        plt.legend().draggable()
        plt.xlabel('x')
        plt.ylabel('f(x)')
        plt.grid()

        
    plt.title('Function: sin(10r), Hidden layer size: '+str(hidden_size)+', DS size: '\
        +str(N)+ ', Initial LR: '+str(initialLearningrate)+', LR decay: '+str(decay), color='b')
evalFunc(dsNonLinear)
plt.show()
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

def printError(ds, label):
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

ds = SupervisedDataSet( 3, 1 )
parameters = []
trains = []
tests = []
for i in range(2, 15):
    parameters.append(i**3)
    N = i
    outputMax = -np.inf
    outputMin = np.inf

    for j in range(N):
        for i in range(N):
            for k in range(N):
                input = [i,j, k]
                output = 2*i + 3*j + k
                ds.appendLinked(input ,  output)
                if output > outputMax:
                    outputMax = output
                if outputMin > output:
                    outputMin = output
    epochsNums = []
    tstdata, trndata = ds.splitWithProportion( 0.25 )
    hidden_size = 15
    
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
    epochsNum = 40
    trainer.trainUntilConvergence( verbose = True, validationProportion = 0.15, maxEpochs = epochsNum, continueEpochs = 10 )
    
    trains.append(printError(trndata, 'trndata'))
    tests.append(printError(tstdata, 'tstdata'))
    epochsNums.append(epochsNum)
    #print n.activateOnDataset(tstdata)

plt.plot(parameters, trains, label='train')
plt.plot(parameters, tests, label='test')
plt.legend().draggable()
plt.title('Dataset size influance (40 epochs, linear function)')
plt.xlabel('Dataset size ')
plt.ylabel('Normalized RMSE')
plt.grid()
plt.show()
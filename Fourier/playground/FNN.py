import numpy as np
from pybrain.tools.shortcuts import buildNetwork
from pybrain.structure import TanhLayer
from pybrain.datasets import SupervisedDataSet
from pybrain.supervised.trainers import BackpropTrainer
from pybrain.utilities           import percentError
from pybrain.structure import LinearLayer, SigmoidLayer
from pybrain.structure import FeedForwardNetwork
from pybrain.structure import FullConnection

from sklearn.metrics import mean_squared_error



def calc():
    filePath = 'asc_gyro_l.skl'
    f = open(filePath, 'r')
    headers = f.readline().split()
    indices = [2]
    numOfFeatures = len(indices)#len(ancestorMap)
    ds = SupervisedDataSet(numOfFeatures, 1)
    press0 = []
    press1 = []
    for line in f:
        splited = line.split()
        output = [float(splited[2]) - 32920.0]#, splited[3]]
        press0.append(float(output[0]))
        #press1.append(float(output[1]))
        input = np.array(splited)
        input = input[indices]#getAnccestorRelativePos(splited)#splited[7:]#
        ds.appendLinked(output[0], output)
    tstdata, trndata = ds.splitWithProportion( 0.25 )
    
    #for n in range(5):
    numOfHidden = 1#15*n + 1
    net = buildNetwork(numOfFeatures, numOfHidden, 1, bias=True)
    #net = FeedForwardNetwork()
    """
    inLayer = LinearLayer(numOfFeatures)
    hiddenLayer0 = SigmoidLayer(numOfHidden)
    #hiddenLayer1 = SigmoidLayer(numOfHidden)
    #hiddenLayer2 = SigmoidLayer(numOfHidden)
    outLayer = LinearLayer(1)
    
    net.addInputModule(inLayer)
    net.addModule(hiddenLayer0)
    #net.addModule(hiddenLayer1)
    #net.addModule(hiddenLayer2)
    net.addOutputModule(outLayer)
    
    in_to_hidden = FullConnection(inLayer, hiddenLayer0)
    #zero2one = FullConnection(hiddenLayer0, hiddenLayer1)
    #one2two = FullConnection(hiddenLayer1, hiddenLayer2)
    hidden_to_out = FullConnection(hiddenLayer0, outLayer)
    
    
    net.addConnection(in_to_hidden)
    #net.addConnection(zero2one)
    #net.addConnection(one2two)
    net.addConnection(hidden_to_out)
    net.sortModules()
    """
    trainer = BackpropTrainer(net, tstdata)
    print 'numOfHidden: ' + str(numOfHidden)
    #res = trainer.trainUntilConvergence()
    for i in range(100):
        res = trainer.train()
    evaluatedData = tstdata
    press0 = []
    press1 = []
    expectedPress0 = []
    expectedPress1 = []
    for input, expectedOutput in evaluatedData:
        output = net.activate(input)
        press0.append(output)
        #press1.append(output[1])
        expectedPress0.append(expectedOutput)
        #expectedPress1.append(expectedOutput[1])
        #errorSum0+=abs(output[0]-expectedOutput[0])
        #errorSum1+=abs(output[1]-expectedOutput[1])
    
    #print errorSum0/len(evaluatedData)
    #print errorSum1/len(evaluatedData)
    print mean_squared_error(press0, expectedPress0)
    print np.mean(expectedPress0)
    #print mean_squared_error(press1, expectedPress1)
    
    """
    arr = np.array(press0)
    print np.std(arr, axis=0)
    arr = np.array(press1)
    print np.std(arr, axis=0)
    print 'end'
    """

#calc()
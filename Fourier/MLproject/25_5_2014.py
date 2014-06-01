from pybrain.structure import FeedForwardNetwork
from pybrain.structure import LinearLayer, SigmoidLayer
from pybrain.structure import FullConnection
from pybrain.datasets import SupervisedDataSet
from pybrain.supervised.trainers import BackpropTrainer
from pybrain.structure.modules import BiasUnit
from pybrain.tools.neuralnets import NNregression
from pybrain.tools.shortcuts import buildNetwork

ds = SupervisedDataSet( 1, 1 )
for i in range(20):
    ds.appendLinked( [i], [i] )
tstdata, trndata = ds.splitWithProportion( 0.25 )
"""
hidden_size = 1   
net = buildNetwork( 1, hidden_size, 1, bias = True )
trainer = BackpropTrainer( net, trndata )
trainer.trainUntilConvergence( verbose = True, validationProportion = 0.15, maxEpochs = 1000, continueEpochs = 10 )
print trndata
print net.activateOnDataset( trndata )
print net.params


"""
inLayer = LinearLayer(1)
hiddenLayer = SigmoidLayer(10)
outLayer = LinearLayer(1)
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


trainer = BackpropTrainer(n, trndata, momentum=0.9)#, verbose=True, weightdecay=0)
#print n.params
trainer.trainEpochs(10)
#print n.params
print trndata
print n.activateOnDataset(trndata)
#trainer.trainUntilConvergence(trndata, 100)


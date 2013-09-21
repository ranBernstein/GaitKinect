from pybrain.structure import LinearLayer, SigmoidLayer
from pybrain.structure import FullConnection
from pybrain.structure import RecurrentNetwork

net = RecurrentNetwork()
net.addInputModule(LinearLayer(2, name='in'))
net.addModule(SigmoidLayer(3, name='hidden'))
net.addOutputModule(LinearLayer(1, name='out'))
net.addConnection(FullConnection(net['in'], net['hidden'], name='c1'))
net.addConnection(FullConnection(net['hidden'], net['out'], name='c2'))

net.addRecurrentConnection(FullConnection(net['hidden'], net['hidden'], name='c3'))

net.sortModules()
print net.activate((2, 2))
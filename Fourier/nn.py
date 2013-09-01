from pybrain.tools.shortcuts import buildNetwork
from pybrain.structure import TanhLayer
from pybrain.datasets import SupervisedDataSet
from pybrain.supervised.trainers import BackpropTrainer

net = buildNetwork(2, 3, 2, bias=True, hiddenclass=TanhLayer)
ds = SupervisedDataSet(2, 2)
ds.addSample((0, 0), (0,0))
ds.addSample((0, 1), (1,1))
ds.addSample((1, 0), (1,0))
ds.addSample((1, 1), (0,1))
trainer = BackpropTrainer(net, ds)


res = trainer.trainUntilConvergence()
print res



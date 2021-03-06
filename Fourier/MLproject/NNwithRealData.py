from pybrain.structure import FeedForwardNetwork
from pybrain.structure import LinearLayer, SigmoidLayer
from pybrain.structure import FullConnection
from pybrain.datasets import SupervisedDataSet, ClassificationDataSet
from pybrain.supervised.trainers import BackpropTrainer
from pybrain.structure.modules import BiasUnit
from pybrain.utilities import percentError
from pybrain.tools.shortcuts import buildNetwork
import math
import utils.interpulation as inter
import numpy as np
import matplotlib.pyplot as plt

lenVec = 100
joints = ['lowerback', 'upperback','thorax' , 'lowerneck', 'upperneck',  \
          'head',  'rhumerus', 'rradius', 'rwrist', 'rhand', 'rfingers', \
          'rthumb', 'lclavicle','lhumerus','lradius','lwrist','lhand','lfingers',\
          'rfemur','rtibia','rfoot','rtoes','lfemur','ltibia','lfoot','ltoes']

timeStampLen= 52
def getData(fileName, vecSize):
    f  = open(fileName, 'r')
    all = []
    map = {}
    for line in f:
        splited = line.split()
        if len(splited) == 0:
            continue
        jointName = splited[0]
        if jointName in joints:
            if not jointName in map:#initialization 
                map[jointName] = []
                for _ in splited[1:]:
                    map[jointName].append([])
            for i,l in enumerate(map[jointName]):
                l.append(float(splited[1+i]))
                #map[jointName][i].append(a)  
                #except:
                #   pass
    ret = []
    for joint,vecs in map.items():
        for vec in vecs:
            _, uniformlySampled = inter.getUniformSampled(range(len(vec)), vec, vecSize)
            """
            maxV = np.max(uniformlySampled)
            minV = np.min(uniformlySampled)
            amp = maxV -minV
            if amp==0:
                print 'zeroi input'
            else:
                uniformlySampled = [2*v/amp -1 for v in uniformlySampled]
            """
            ret = ret + uniformlySampled.tolist()
    """      
    ret = []
    for i in xrange(0, len(all), vecSize):
        ret.append(all[i:i+vecSize])
    """
    return ret

vecSize =  100
subjects = [2, 5, 6, 7, 8, 12, 16, 35 ,39]
ds = None
for s in subjects:
    for cycleNum in range(1, 13):
        fileName = '../inputs/Vicon from CMU/subjects/'+str(s)+'/'+str(cycleNum)+'.amc'
        try:
            data = getData(fileName, vecSize)
        except IOError:
            continue
        if ds is None:#initialization
            ds = ClassificationDataSet( len(data), 1 )
        ds.appendLinked(data ,  subjects.index(s))
ds.nClasses = len(subjects)

decay= 0.99995
myWeightdecay = 0.8
initialLearningrate= 0.005
hidden_size = 1000
epochs=1000
splitProportion = 0.5

print 'dataset size', len(ds)
print 'input layer size', len(ds.getSample(0)[0])
tstdata, trndata = ds.splitWithProportion( splitProportion )
trndata._convertToOneOfMany( )
tstdata._convertToOneOfMany( )

print "Number of training patterns: ", len(trndata)
print "Input and output dimensions: ", trndata.indim, trndata.outdim
print "First sample (input, target, class):"
print trndata['input'][0], trndata['target'][0], trndata['class'][0]

#for lr in [0.0001]:#20, 40, 80, 160]:
#for lr in [0.006, 0.003, 0.0015, 0.0007, \
           #0.0003, 0.0001, 0.00005]: 
 
inLayer = LinearLayer(len(trndata.getSample(0)[0]))
hiddenLayer = SigmoidLayer(hidden_size)
outLayer = LinearLayer(len(trndata.getSample(0)[1]))
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

trainer = BackpropTrainer(n, trndata,  learningrate=initialLearningrate,\
                            lrdecay=decay, verbose=True, weightdecay=myWeightdecay)
print 'h: ', hidden_size, ' epochs ', epochs, ' initialLearningrate ', \
    initialLearningrate, ' decay ', decay, ' splitProportion: ', \
    str(splitProportion), ' weightdecay ', str(myWeightdecay)
for _ in range(epochs):
    trainer.trainEpochs(1)
    trnresult = percentError( trainer.testOnClassData(),
                                  trndata['class'] )
    tstresult = percentError( trainer.testOnClassData(
           dataset=tstdata ), tstdata['class'] )
    
    print "epoch: %4d" % trainer.totalepochs, \
      "  train error: %5.2f%%" % trnresult, \
      "  test error: %5.2f%%" % tstresult












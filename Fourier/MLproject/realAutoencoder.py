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
dsForFiles = {} 
for s in subjects:
    for cycleNum in range(1, 13):
        fileName = '../inputs/Vicon from CMU/subjects/'+str(s)+'/'+str(cycleNum)+'.amc'
        try:
            data = getData(fileName, vecSize)
        except IOError:
            continue
        if ds is None:#initialization
            ds = ClassificationDataSet( len(data), len(data) )
        dsForFiles[str(data)] = s
        ds.appendLinked(data ,  data)
ds.nClasses = len(data)
decay= 0.9999
myWeightdecay = 0.8
initialLearningrate= 0.00025
hidden_size = 500
epochs=40
splitProportion = 0.5
description ='AutoEncoder convergence, hidden layer size: '+str(hidden_size) 

print 'dataset size', len(ds)
print 'input layer size', len(ds.getSample(0)[0])
tstdata, trndata = ds.splitWithProportion( splitProportion )
#trndata._convertToOneOfMany( )
#tstdata._convertToOneOfMany( )
"""
print "Number of training patterns: ", len(trndata)
print "Input and output dimensions: ", trndata.indim, trndata.outdim
print "First sample (input, target, class):"
print trndata['input'][0], trndata['target'][0], trndata['class'][0]
"""
#for lr in [0.0001]:#20, 40, 80, 160]:
#for lr in [0.006, 0.003, 0.0015, 0.0007, \
           #0.0003, 0.0001, 0.00005]:  
inLayer = LinearLayer(len(trndata.getSample(0)[0]))
hiddenLayer = SigmoidLayer(hidden_size)
outLayer = LinearLayer(len(trndata.getSample(0)[0]))
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
def printError(ds, label):
    sum = 0
    for input, output in ds:
        pred = n.activate(input)
        sum+= np.sqrt(np.sum(np.square(output - pred)))/np.sqrt(np.sum(np.square(output)))
    #print input, pred
    mrmse = sum/len(ds)
    print label, 'MRMSE: ', mrmse
    return mrmse
trnresults=[]
tstresults=[]
for _ in range(epochs):
    trainer.trainEpochs(1)
    trnresults.append(printError(trndata, 'train'))
    tstresults.append(printError(tstdata, 'test'))
  
an = FeedForwardNetwork()
an.addInputModule(inLayer)
an.addOutputModule(hiddenLayer)
an.addModule(b)
an.addConnection(in_to_hidden)
an.addConnection(b_to_hidden)
an.sortModules()
#print len(in_to_hidden

subjects = [2, 5, 6, 7, 8, 12, 16, 35 ,39]

#train
def createFile(label, ds):
    out = open(label+'RealOutH_'+str(hidden_size)+'.arff', 'w')
    out.write('@relation weka.kuku\n\n')
    for i in range(hidden_size):
        out.write('@attribute a'+str(i)+ ' numeric\n')
    st=''
    for i,s in enumerate(subjects):
        st+=str(s)
        if i!= len(subjects)-1:
            st+=','
    out.write('@attribute class {'+st+'}\n\n@data\n\n')
    
    for input, tag in ds:
        newInput= an.activate(input)
        for v in newInput:
            out.write(str(v)+',')
        out.write(str(dsForFiles[str(data)])+'\n')

createFile('train', trndata)
createFile('test', tstdata)
plt.plot(trnresults, label='Train error ')
plt.plot(tstresults, label='Test error ')
plt.title(description)
plt.xlabel('epoches')
plt.ylabel('error')
plt.legend().draggable()


plt.show()









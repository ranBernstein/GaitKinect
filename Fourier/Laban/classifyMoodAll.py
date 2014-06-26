from pybrain.structure import FeedForwardNetwork
from pybrain.structure import LinearLayer, SigmoidLayer
from pybrain.structure import FullConnection
from pybrain.datasets import ClassificationDataSet
from pybrain.supervised.trainers import BackpropTrainer
from pybrain.structure.modules import BiasUnit
from pybrain.utilities import percentError
import numpy as np
import matplotlib.pyplot as plt
import algorithm.generalExtractor as ge

vecSize =  100
ds = None
tests = []
sds = []
coupels = [['sad', 'fear']]
ms = np.linspace(0, 1, 50)
#for m in ms:
#hidden_size = int(hidden_size)
moods = ['anger', 'fear', 'happy', 'sad']#, 'neutral']
trnresults = []
tstresults=[]
excpectedLens = []
for m,mood in enumerate(moods):
    trnresults.append([])
    tstresults.append([])
    #hits[m].append(0)
    excpectedLens.append(0)
    #for mood in couple:
    for typeNum in range(1,21):
        for take in range(1,10):
            fileName = '../inputs/Rachelle/v2/recordingsByMood/'+mood+'/'+\
            str(typeNum)+'_'+str(take)+'.skl'
            try:
                data = ge.getFeatureVec(fileName)
            except IOError:
                continue
            if ds is None:#initialization
                ds = ClassificationDataSet( len(data), 1 )
            excpectedLens[m]+=1
            ds.appendLinked(data ,  moods.index(mood))
splitProportion = 0.2
decay= 0.99993
myWeightdecay = 0.5
initialLearningrate= 0.01
hidden_size = 200
epochs=1000
momentum=0.15
ds.nClasses = len(moods)
tstdata, trndata = ds.splitWithProportion( splitProportion )
trndata._convertToOneOfMany( )
tstdata._convertToOneOfMany( )
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

trainer = BackpropTrainer(n, trndata, learningrate=initialLearningrate,\
    lrdecay=decay, verbose=True, weightdecay=myWeightdecay, momentum=momentum)
description =  'all: ds '+ str(len(ds))+\
 ', h: '+ str(hidden_size)+ \
 ', lr ' + str(initialLearningrate) 
description =   description+ ', decay ' +  str(decay) + ' sp: ' +   str(splitProportion) + \
' wd ' +  str(myWeightdecay)+ ' momentum ' + str(momentum)
print description
trnresults=[]
tstresults=[]
for _ in range(epochs):
    trainer.trainEpochs(1)
    
    trnresult = percentError( trainer.testOnClassData(),
                                  trndata['class'] )
    trnresults.append(trnresult)
    tstresult = percentError( trainer.testOnClassData(
           dataset=tstdata ), tstdata['class'] )
    tstresults.append(tstresult)
    print "epoch: %4d" % trainer.totalepochs, \
      "  train error: %5.2f%%" % trnresult, \
      "  test error: %5.2f%%" % tstresult
    
      
    def eval(ds, label):
        h=[]
        expected=[]
        for m in moods:
            h.append(0)
            expected.append(0)
        for inpt, tag in ds:
            res = np.array(n.activate(inpt))
            guess = np.argmax(res)
            tag = np.argmax(tag)
            expected[tag]+=1
            if tag == guess:
                h[tag]+=1
        for m,v in zip(moods,h):
            #print v, tag, len(hits), len(excpectedLens)
            #hits[tag].append(float(v)/excpectedLens[tag])
            print label, m, v, expected[moods.index(m)]
    eval(trndata, 'train data')
    eval(tstdata, 'test data')
    
#tests.append(min(tstresults[-100:]))
#sds.append(np.std(min(tstresults[-100:])))

plt.figure()
#for m,_ in enumerate(moods):
plt.plot(trnresults, label='Train error')
plt.plot(tstresults, label='Test error')
plt.title(description)
plt.xlabel('epoches')
plt.ylabel('error')
plt.legend().draggable()
"""
plt.figure()
plt.plot(ms, tests)
plt.title('test error vs momentum')

plt.figure()
plt.plot(ms, sds)
plt.title('sds vs momentum')
"""
plt.show()











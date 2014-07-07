
from pybrain.supervised.trainers import BackpropTrainer
from pybrain.utilities import percentError
import numpy as np
import matplotlib.pyplot as plt
import LabanUtils.util as labanUtil
import LabanUtils.combinationsParser as cp

qualities, combinations = cp.getCombinations()
ds = labanUtil.getPybrainDataSet()
inLayerSize = len(ds.getSample(0)[0])
outLayerSize = len(ds.getSample(0)[1])
splitProportion = 0.2
decay= 0.99991
myWeightdecay = 0.99999
initialLearningrate= 0.001
hiddenSize = 100
epochs=50
momentum=0#.25
#ds.nClasses = len(qualities)
tstdata, trndata = ds.splitWithProportion( splitProportion )
res = labanUtil.constructNet(inLayerSize, hiddenSize, outLayerSize)
n=res[0]
trainer = BackpropTrainer(n, trndata, learningrate=initialLearningrate,\
    lrdecay=decay, verbose=True, weightdecay=myWeightdecay, momentum=momentum)
description =  'ds '+ str(len(ds))+\
 ', h: '+ str(hiddenSize)+ \
 ', lr ' + str(initialLearningrate) 
description =   description+ ', decay ' +  str(decay) + ' sp: ' +   str(splitProportion) + \
' wd ' +  str(myWeightdecay)+ ' momentum ' + str(momentum)
print description
trnresults =[]
tstresults = []
q=5
for _ in range(epochs/q):
    #trainer.trainEpochs(1)
    trainer.trainUntilConvergence(dataset=trndata, \
            maxEpochs=q, verbose=True, validationProportion=0.1)
    def eval(ds):
        s=0.0
        for inpt, tag in ds:
            res = n.activate(inpt)
            res = [1 if r > 0.5 else 0 for r in res]
            res = np.array(res)
            
            s += sum(np.abs(res - tag))
        s=s/len(tag)/len(ds)
        return s
    trnresults.append(eval(trndata))
    tstresults.append(eval(tstdata))
    
    """
    def bucket(ds, label):
        h=np.zeros(np.shape(qualities))
        for inpt, tag in ds:
            res = n.activate(inpt)
            res = [1 if r > 0.5 else 0 for r in res]
            res = np.array(res)
            tag = np.array(tag)
            h+= np.abs(tag-res)
            #guess = np.argmax(res)
            #tag = np.argmax(tag)
            #expected[tag]+=1
            #if tag == guess:
                #h[tag]+=1
        h/=len(ds)
        for i,q in enumerate(qualities):
            #print v, tag, len(hits), len(excpectedLens)
            #hits[tag].append(float(v)/excpectedLens[tag])
            print label, q, h[i]
    bucket(trndata, 'train data')
    bucket(tstdata, 'test data')
    """
    """
    trnresult = percentError( trainer.testOnClassData(),
                                  trndata['class'] )
    trnresults.append(trnresult)
    tstresult = percentError( trainer.testOnClassData(
           dataset=tstdata ), tstdata['class'] )
    tstresults.append(tstresult)
    print "epoch: %4d" % trainer.totalepochs, \
      "  train error: %5.2f%%" % trnresult, \
      "  test error: %5.2f%%" % tstresult
    """
#tests.append(min(tstresults[-100:]))
#sds.append(np.std(min(tstresults[-100:])))
#plt.figure()
plt.plot(trnresults, label='Train error')
plt.plot(tstresults, label='Test error')
plt.title('Laban Classification with threshold 0.5')
plt.xlabel('epoches')
plt.ylabel('error')
plt.legend().draggable()
plt.show()











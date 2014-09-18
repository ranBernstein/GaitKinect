
from pybrain.supervised.trainers import BackpropTrainer
from pybrain.utilities import percentError
import numpy as np
import matplotlib.pyplot as plt
import LabanUtils.util as labanUtil
import LabanUtils.combinationsParser as cp
from sklearn import metrics

qualities, combinations = cp.getCombinations()
ds, featuresNames = labanUtil.getPybrainDataSet()
inLayerSize = len(ds.getSample(0)[0])
outLayerSize = len(ds.getSample(0)[1])
splitProportion = 0.2
decay= 0.999995
myWeightdecay = 0.00015#0.99999
initialLearningrate= 0.01
hiddenSize = 150
epochs=3000
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
    """
    def eval(ds):
        s=0.0
        for inpt, tag in ds:
            res = n.activate(inpt)
            res = [1 if r > 0.5 else 0 for r in res]
            res = np.array(res)
            
            s += sum(np.abs(res - tag))
        s=s/len(tag)/len(ds)
        return s
    """
    def eval(ds):
        f1s=[]
        pred = n.activateOnDataset(ds)
        X, Y = labanUtil.fromDStoXY(ds)
        for i,y in enumerate(Y):
            f1s.append(metrics.f1_score(np.round(y), np.round(pred[:,i])))
        return np.mean(f1s)
    trnresults.append(eval(trndata))
    tstresults.append(eval(tstdata))
    
plt.plot(trnresults, label='Train error')
plt.plot(tstresults, label='Test error')
plt.title('Laban Classification with threshold 0.5')
plt.xlabel('epoches')
plt.ylabel('error')
plt.legend().draggable()
plt.show()











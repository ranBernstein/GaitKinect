from pybrain.supervised.trainers import BackpropTrainer
from pybrain.utilities import percentError
import numpy as np
import matplotlib.pyplot as plt
import LabanUtils.util as labanUtil
import LabanUtils.combinationsParser as cp
from pybrain.structure import FeedForwardNetwork
import matplotlib.pyplot as plt
from sklearn import svm

qualities, combinations = cp.getCombinations()
ds = labanUtil.getPybrainDataSet()
inLayerSize = len(ds.getSample(0)[0])
outLayerSize = len(ds.getSample(0)[1])
splitProportion = 0.2
decay= 0.99991
myWeightdecay = 0.99999
initialLearningrate= 0.001
hiddenSize = 1
epochs=10
momentum=0#.25
#ds.nClasses = len(qualities)
tstdata, trndata = ds.splitWithProportion( splitProportion )
svmAloneScore = labanUtil.clfSVM(tstdata, trndata)

n, inLayer, hiddenLayer, b, in_to_hidden, b_to_hidden = \
    labanUtil.constructNet(inLayerSize, hiddenSize, outLayerSize)
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
q=1
scores=[]
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
    
    an = FeedForwardNetwork()
    an.addInputModule(inLayer)
    an.addOutputModule(hiddenLayer)
    an.addModule(b)
    an.addConnection(in_to_hidden)
    an.addConnection(b_to_hidden)
    an.sortModules()
    #print len(in_to_hidden
    
    clfs = []
    for _ in qualities:
        clf = svm.SVC()
        clfs.append(clf)
    
    def fromDStoXY(ds):
        X=[]
        Y=[]
        for _ in qualities:
            Y.append([])
        for input, tag in ds:
            input = an.activate(input)
            X.append(input)
            for i,_ in enumerate(qualities):
                Y[i].append(tag[i])
        return X,Y
    X,Y  = fromDStoXY(trndata)
    for i,y in enumerate(Y):
        clfs[i].fit(X,y)
    
    X,Y  = fromDStoXY(tstdata)
    localScores = []
    for i,q in enumerate(qualities):
        localScores.append(clfs[i].score(X,Y[i]))
    score = np.mean(localScores)
    scores.append(1-score)
    print score

plt.plot(trnresults, label='Train error: ' + str(trnresults[-1]))
plt.plot(tstresults, label='Test error: ' + str(tstresults[-1]))
plt.plot(scores, label='SVM+net train: '+str(scores[-1]))
plt.plot([svmAloneScore]*len(scores),  label='SVM'+str(scores[-1]))
plt.title('Laban Classification with threshold 0.5 vs svm')
plt.xlabel('epoches')
plt.ylabel('error')
plt.legend().draggable()

X,Y = fromDStoXY(trndata)
for i,y in enumerate(Y):
    plt.figure()
    plt.scatter(X, y)
    plt.show()











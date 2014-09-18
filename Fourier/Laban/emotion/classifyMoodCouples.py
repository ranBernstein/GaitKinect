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
tests = []
sds = []
#coupels = [['sad', 'fear']]
#for hidden_size in np.linspace(15, 300, 40):
#hidden_size = int(hidden_size)
coupels = [['anger', 'fear'], ['anger', 'happy'], ['anger', 'sad'], ['happy', 'fear'], ['sad', 'fear'], ['sad', 'happy']]
#moods = ['anger', 'fear']#, 'happy', 'sad', 'neutral']
for couple in coupels:
#for mood in moods:
    ds = None
    for mood in couple:
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
                ds.appendLinked(data ,  couple.index(mood))
    splitProportion = 0.2
    decay= 0.9999
    myWeightdecay = 1#0.75
    initialLearningrate= 0.002
    hidden_size = 75
    epochs=1000
    momentum=0.25
    ds.nClasses = len(couple)
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
    description =  'ds '+ str(len(ds))+\
     ', h: '+ str(hidden_size)+ \
     ', lr ' + str(initialLearningrate) 
    description =   description+ ', decay ' +  str(decay) + ' sp: ' +   str(splitProportion) + \
    ' wd ' +  str(myWeightdecay)+ ' momentum ' + str(momentum)
    print description
    trnresults =[]
    tstresults = []
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
          "  test error: %5.2f%%" % tstresult, str(couple)
    tests.append(np.mean(tstresults[-10:]))
    sds.append(np.std(tstresults[-10:]))
    #plt.plot(trnresults, label='Train error of '+ str(couple))
    plt.plot(tstresults, label='Test error of '+ str(couple))
plt.title(description)
plt.xlabel('epoches')
plt.ylabel('error')
plt.legend().draggable()
print tests
print sds
plt.figure()
plt.scatter(range(len(tests)), tests)
plt.title('Final test errors')

plt.figure()
plt.scatter(range(len(sds)), sds)
plt.title('Final sd')

plt.show()











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
import combinationsParser as cp

vecSize =  100
tests = []
sds = []
qualities, combinations = cp.getCombinations()
moods = combinations.keys()
for hidden_size in np.linspace(20, 400, 25):
    hidden_size = int(hidden_size)
    
    ds = None
    for mood in moods:
        for typeNum in range(1,21):
            for take in range(1,10):
                fileName = '../inputs/Rachelle/v2/recordingsByMood/'+mood+'/'+\
                str(typeNum)+'_'+str(take)+'.skl'
                try:
                    data = ge.getFeatureVec(fileName)
                except IOError:
                    continue
                if ds is None:#initialization
                    ds = ClassificationDataSet( len(data), len(qualities) )
                output = np.zeros((len(qualities)))
                for q in combinations[mood][typeNum]:
                    output[qualities.index(q)] = 1
                ds.appendLinked(data ,  output)
    splitProportion = 0.2
    decay= 0.99991
    myWeightdecay = 0.99999
    initialLearningrate= 0.001
    #hidden_size = 300
    epochs=1000
    momentum=0#.25
    ds.nClasses = len(qualities)
    tstdata, trndata = ds.splitWithProportion( splitProportion )
    #trndata._convertToOneOfMany( )
    #tstdata._convertToOneOfMany( )
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
    q=5
    for _ in range(epochs/q):
        #trainer.trainEpochs(1)
        trainer.trainUntilConvergence(dataset=trndata, \
                maxEpochs=q, verbose=True, validationProportion=0.1)
        def eval(ds):
            s=0.0
            for inpt, tag in ds:
                res = np.array(n.activate(inpt))
                s += sum(np.abs(res - tag))
            s=s/len(tag)/len(ds)
            return s
        trnresults.append(eval(trndata))
        tstresults.append(eval(tstdata))
        
        def bucket(ds, label):
            h=np.zeros(np.shape(qualities))
            """
            expected=[]
            for q in qualities:
                h.append(0)
                expected.append(0)
            """
            for inpt, tag in ds:
                res = np.array(n.activate(inpt))
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
    plt.title('Laban: '+description)
    plt.xlabel('epoches')
    plt.ylabel('error')
    plt.legend().draggable()
plt.show()











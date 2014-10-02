import combinationsParser as cp
from pybrain.datasets import ClassificationDataSet
import Laban.algorithm.generalExtractor as ge
import numpy as np
from pybrain.structure import FeedForwardNetwork
from pybrain.structure import LinearLayer, SigmoidLayer
from pybrain.structure import FullConnection
from pybrain.structure.modules import BiasUnit
def getPybrainDataSet(source='Rachelle'):
    first = False#True
    qualities, combinations = cp.getCombinations()
    moods = combinations.keys()
    ds = None
    l=0
    for mood in moods:
        if mood=='neutral':
            continue
        for typeNum in range(1,21):
            for take in range(1,10):
                fileName = 'recordings/'+source+'/'+mood+'/'+\
                str(typeNum)+'_'+str(take)+'.skl'
                try:
                    data, featuresNames = ge.getFeatureVec(fileName, first)
                    first = False
                except IOError:
                    continue
                if ds is None:#initialization
                    ds = ClassificationDataSet( len(data), len(qualities) )
                output = np.zeros((len(qualities)))
                for q in combinations[mood][typeNum]:
                    output[qualities.index(q)] = 1
                ds.appendLinked(data ,  output)

                l+=sum(output)
    return ds, featuresNames

def constructNet(inLayerSize, hiddenSize, outLayerSize):
    inLayer = LinearLayer(inLayerSize)
    hiddenLayer = SigmoidLayer(hiddenSize)
    outLayer = SigmoidLayer(outLayerSize)
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
    
    return n, inLayer, hiddenLayer, b, in_to_hidden, b_to_hidden

def fromDStoXY(ds):
    outLayerSize = len(ds.getSample(0)[1])
    X=[]
    Y=[]
    for _ in range(outLayerSize):
        Y.append([])
    for input, tag in ds:
        X.append(input)
        for i in range(outLayerSize):
            Y[i].append(tag[i])
    return np.array(X),np.array(Y)

"""
def clfSVM(tstdata, trndata):
    outLayerSize = len(tstdata.getSample(0)[1])
    clfs = []
    for _ in range(outLayerSize):
        clf = svm.SVC()
        clfs.append(clf)
    
   
    X,Y  = fromDStoXY(trndata)
    for i,y in enumerate(Y):
        clfs[i].fit(X,y)
    
    X,Y  = fromDStoXY(tstdata)
    localScores = []
    for i in range(outLayerSize):
        localScores.append(clfs[i].score(X,Y[i]))
    return 1-np.mean(localScores)
"""
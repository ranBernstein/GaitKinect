from sklearn.tree import DecisionTreeClassifier, export_graphviz
import numpy as np
import util as labanUtil
import combinationsParser as cp
from sklearn.feature_selection import f_classif
from StringIO import StringIO
import pydot
import math  


def bestByInfoGain(X, y, featuresNames):
    importances = infoGain(X, y)
    bestFeatureName = featuresNames[np.argmax(importances)]
    return max(importances), bestFeatureName

def createDiagram(X, y, featuresNames, fileName='out.pdf'):
    X = np.array(X)
    #qualities, combinations = cp.getCombinations()
    clf = DecisionTreeClassifier(criterion='entropy')
    clf.fit(X,y)
    out = StringIO()
    out = export_graphviz(clf, feature_names=featuresNames, out_file=out)
    print out
    value = out.getvalue()
    graph = pydot.graph_from_dot_data(value) 
    graph.write_pdf(fileName+'.pdf') 

def recursiveRanking(X, y):
    X = np.array(X)
    featuresNum = X.shape[1]
    clf = DecisionTreeClassifier(criterion='entropy')
    ranks = []
    ranksSet = set()
    tmp = X
    dic={}
    for i in range(featuresNum):
        clf.fit(tmp,y)
        importances = clf.tree_.compute_feature_importances()
        best = np.argmax(importances)
        if not best in ranksSet:
            ranks.append(best)
            ranksSet.add(best)
            tmp[:,best] = np.zeros(tmp.shape[0])
            dic[best] = i
        """
        if best+1 < tmp.shape[1]:
            tmp = np.concatenate((tmp[:,:best], tmp[:, best+1:]),axis=1)
        else:
            tmp = tmp[:,:best]
        """
    """
    new = ranks[:1]
    for i,r in enumerate(ranks):
        if i==0:
            continue
        left = ranks[:i]
        m = min(left)
        while m<=r and len(left)>0:
            r+=1
            del left[np.argmin(left)]
            if len(left)==0:
                break
            m = min(left)
        new.append(r)
    ranks = new
    """
    new = np.ones(featuresNum)
    for f in range(featuresNum):
        if f in dic:
            r = dic[f]
            val = 1.0/(r+1)
            #print f, r, val
        else:
            val=0
            #print f, val
        new[f] = val
    fValues, pValues = f_classif(X, y)
    return new, pValues
    
def getEntropy(D):
    """
    Calculate and return entropy of 1-dimensional numpy array D 
    """
    length=D.size
    valueList=list(set(D))
    numVals=len(valueList)
    countVals=np.zeros(numVals)
    Ent=0
    for idx,val in enumerate(valueList):
        countVals[idx]=np.count_nonzero(D==val)
        Ent+=countVals[idx]*1.0/length*np.log2(length*1.0/countVals[idx])
    return Ent

def featureInfoGain(X,y,feat):
    """ 
    Calculate maximum information gain w.r.t. the feature which is specified in column feat of the 2-dimensional array X.
    """
    EntWithoutSplit=getEntropy(y)
    feature=X[:,feat]
    length=len(feature)
    valueList=list(set(feature))
    splits=np.diff(valueList)/2.0+valueList[:-1]
    maxGain=0
    bestSplit=0
    bestPart1=[]
    bestPart2=[]
    for split in splits:
        Part1idx=np.argwhere(feature<=split)
        Part2idx=np.argwhere(feature>split)
        E1=getEntropy(y[Part1idx[:,0]])
        l1=len(Part1idx)
        E2=getEntropy(y[Part2idx[:,0]])
        l2=len(Part2idx)
        Gain=EntWithoutSplit-(l1*1.0/length*E1+l2*1.0/length*E2)
        if Gain > maxGain:
            maxGain=Gain
            bestSplit=split
            bestPart1=Part1idx
            bestPart2=Part2idx
    return maxGain#,bestSplit,bestPart1,bestPart2  

def infoGain(X,y):
    X = np.array(X)
    gains = []
    featureNum = X.shape[1]
    for f in range(featureNum):
        gains.append(featureInfoGain(X,y,f))
    fValues, pValues = f_classif(X, y)
    return gains, pValues
"""
trainSource = 'Karen'
trndata, featuresNames = labanUtil.getPybrainDataSet(trainSource)  
X, Y = labanUtil.fromDStoXY(trndata)
y=Y[0]
X, y = np.array([[1,1,0,0], [1,0,0,2], [0,0,0,1]]), np.array([1,0,1])
print infoGain(X,y)
"""


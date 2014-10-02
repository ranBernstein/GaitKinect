import LabanUtils.util as labanUtil
from sklearn.ensemble import AdaBoostClassifier
import LabanUtils.combinationsParser as cp
from sklearn.feature_selection import f_classif, SelectKBest
import matplotlib.pyplot as plt
import numpy as np
import mlpy

chooser=f_classif

quality = 'Strong'
trainSource = 'Karen'
testSource = 'Rachelle'
trndata, featuresNames = labanUtil.getPybrainDataSet(trainSource)  
#tstdata, featuresNames = labanUtil.getPybrainDataSet(trainSource)  
X, Y = labanUtil.fromDStoXY(trndata)
#X_test, Y_test = labanUtil.fromDStoXY(tstdata)
f1s=[]
ps =[]
rs=[]
clf = AdaBoostClassifier()
qualities, combinations = cp.getCombinations()
selectedFeaturesNum = 7
qualityIndex = qualities.index(quality)
y = Y[qualityIndex]
samplesNum = len(trndata)

"""
selector = SelectKBest(chooser, samplesNum)
selector.fit(X, y)
support = selector.get_support().tolist()
indices = [i for i, x in enumerate(support) if x == True]
xNew = []
for x in X:
    curr = []
    for i in indices:
        curr.append(x[i])
    xNew.append(curr)
X=xNew
"""

def cor(x01, x02):
    print max(np.correlate(x01,x02))/np.sqrt(np.dot(x01,x01)*np.dot(x02,x02))


pca = mlpy.PCA()
pca.learn(np.array(X))
X = pca.transform(X)

selector = SelectKBest(chooser, 2)
selector.fit(X, y)
support = selector.get_support().tolist()
indices = [i for i, x in enumerate(support) if x == True]
x01 = [x[indices[0]] for i,x in enumerate(X) if y[i]==0]
x02 = [x[indices[1]] for i,x in enumerate(X) if y[i]==0]
x11 = [x[indices[0]] for i,x in enumerate(X) if y[i]==1]
x12 = [x[indices[1]] for i,x in enumerate(X) if y[i]==1]

plt.scatter(x01, x02, c='b')
plt.scatter(x11, x12, c='r')
plt.xlabel(featuresNames[indices[0]])
plt.ylabel(featuresNames[indices[1]])
m0 = np.mean(x01), np.mean( x02)
plt.title(quality)
plt.show()
    
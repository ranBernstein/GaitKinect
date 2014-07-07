from pybrain.supervised.trainers import BackpropTrainer
from pybrain.utilities import percentError
import numpy as np
import matplotlib.pyplot as plt
import LabanUtils.util as labanUtil
import LabanUtils.combinationsParser as cp
from pybrain.structure import FeedForwardNetwork
import matplotlib.pyplot as plt
from sklearn.svm import LinearSVC
from sklearn import metrics
from sklearn.utils.extmath import density
from sklearn import svm
from  sklearn.ensemble import RandomForestClassifier
from sklearn import tree
from sklearn.ensemble import AdaBoostClassifier
from sklearn.ensemble import GradientBoostingClassifier
from utils import MovingAverage as ma
import math

class L1LinearSVC(LinearSVC):

    def fit(self, X, y):
        # The smaller C, the stronger the regularization.
        # The more regularization, the more sparsity.
        self.transformer_ = LinearSVC(penalty="l1",
                                      dual=False, tol=1e-3)
        X = self.transformer_.fit_transform(X, y)
        return LinearSVC.fit(self, X, y)
    
    def predict(self, X):
        X = self.transformer_.transform(X)
        return LinearSVC.predict(self, X)


qualities, combinations = cp.getCombinations()
ds = labanUtil.getPybrainDataSet()
inLayerSize = len(ds.getSample(0)[0])
outLayerSize = len(ds.getSample(0)[1])
splitProportion = 0.2
testNum = 50

#params = np.logspace(math.pow(10, -10), 1, 10)
#eval = 'Learning rate'

params = [1]#range(1,101, 3)
eval = 'nEstimators'

#for p in params:
f1s = []
recalls = []
precisions = []
for _ in range(testNum):
    tstdata, trndata = ds.splitWithProportion( splitProportion )
    X, Y = labanUtil.fromDStoXY(trndata)
    X_test, Y_test = labanUtil.fromDStoXY(tstdata)
    localF1s = []
    localRecalls = []
    localPercisions = []
    for y, y_test in zip(Y, Y_test):
        if all(v == 0 for v in y):
            continue
        #clf = L1LinearSVC()
        #clf = svm.SVC()
        #clf = RandomForestClassifier()
        #clf = tree.DecisionTreeClassifier()
        #clf = AdaBoostClassifier(n_estimators=nEstimators)
        
        clf = GradientBoostingClassifier()#n_estimators=nEstimators, learning_rate=lr)
        
        name = str(clf).split()[0].split('(')[0]
        clf.fit(X, y)
        pred = clf.predict(X_test)
        f1 = metrics.f1_score(y_test, pred)
        recall = metrics.recall_score(y_test, pred)
        localRecalls.append(recall)
        localF1s.append(f1)#np.sum(np.abs(pred-y_test))/float(len(y_test)))
        localPercisions.append(metrics.precision_score(y_test, pred))
    f1s.append(np.mean(localF1s))
    recalls.append(np.mean(localRecalls))
    precisions.append(np.mean(localPercisions))
    
m = np.mean(f1s)
print f1s
print m
#plt.plot(params, scores)
#plt.plot(params, f1s, label='F1 score')
#plt.plot(params, ma.movingAverage(f1s, 4, 1), label='F1 score smoothed')
params=range(testNum)
plt.scatter(params, f1s, label='F1 score')
plt.scatter(params, recalls, label='recall', c='r')
plt.scatter(params, precisions, label='precision', c='b')
plt.legend().draggable()
plt.title(name+', Mean F1: ' + str(m))
plt.show()











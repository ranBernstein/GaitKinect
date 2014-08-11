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
from sklearn.ensemble import ExtraTreesClassifier
from utils import MovingAverage as ma
import math
from multiprocessing import Pool
from sklearn.feature_selection import SelectPercentile, f_classif, f_oneway, f_regression
chooser=f_regression
def eval(ds, p):
    testNum=200
    splitProportion=0.2
    ts=[]
    sts=[]
    for _ in range(testNum):
        tstdata, trndata = ds.splitWithProportion( splitProportion )
        X, Y = labanUtil.fromDStoXY(trndata)
        X_test, Y_test = labanUtil.fromDStoXY(tstdata)
        #localF1s = []
        #localRecalls = []
        #localPercisions = []
        for y, y_test in zip(Y, Y_test):
            if all(v == 0 for v in y):
                continue
            #clf = LinearSVC()#fit_intercept=True, C=p)
            #clf.sparsify()
            
            #clf = RandomForestClassifier(max_depth=8, oob_score=True)#criterion='entropy')
            clf = tree.DecisionTreeClassifier()#max_depth=p)
            #clf = AdaBoostClassifier(n_estimators=60, max_depth=p)
            #clf = GradientBoostingClassifier(n_estimators=60)#, learning_rate=lr)
            #clf = ExtraTreesClassifier(n_estimators=p)
            selector = SelectPercentile(chooser, percentile=p)
            selector.fit(X, y)
            name = str(clf).split()[0].split('(')[0]
            clf.fit(X, y)
            #clf.sparsify()
            #pred = clf.predict(X)
            #tr.append(metrics.f1_score(y, pred))
            pred = clf.predict(X_test)
            ts.append(metrics.f1_score(y_test, pred))
            
            clf.fit(selector.transform(X), y)
            pred = clf.predict(selector.transform(X_test))
            sts.append(metrics.f1_score(y_test, pred))
            #recall = metrics.recall_score(y_test, pred)
            #localRecalls.append(recall)
            #localF1s.append(f1)#np.sum(np.abs(pred-y_test))/float(len(y_test)))
            #localPercisions.append(metrics.precision_score(y_test, pred))
    return np.mean(ts), np.mean(sts), name

if __name__ == '__main__':
    qualities, combinations = cp.getCombinations()
    pool = Pool(7)   
    ds = labanUtil.getPybrainDataSet()
    inLayerSize = len(ds.getSample(0)[0])
    outLayerSize = len(ds.getSample(0)[1])
    tsF1s = []
    stsF1s = []

    maxNumEstimators=300
    #params = np.linspace(0.1, 1, 10)
    params = range(1, 100, 4)
    m = {}
    for i,p in enumerate(params):
        m[i] = pool.apply_async(eval, [ds, p])
    for i,nEstimators in enumerate(params):
        tsF1, stsF1, name = m[i].get()
        tsF1s.append(tsF1)
        stsF1s.append(stsF1)
    m = np.mean(stsF1s)
    print m
    print stsF1s
    plt.plot(params, tsF1s, label='Test')
    plt.plot(params, stsF1s, label=chooser.__name__)

    """
    plt.scatter(params, f1s, label='F1 score')
    plt.scatter(params, recalls, label='recall', c='r')
    plt.scatter(params, precisions, label='precision', c='b')
    """
    plt.legend().draggable()
    plt.title(name+', Mean Test F1: ' + str(m))
    plt.show()











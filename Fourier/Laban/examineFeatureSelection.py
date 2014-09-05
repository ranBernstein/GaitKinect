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
from sklearn.feature_selection import SelectPercentile, f_classif, \
    f_oneway, f_regression, chi2, RFE, RFECV 
from sklearn.svm import LinearSVC    

chooser=f_classif
def eval(ds, testNum, p, splitProportion=0.2):
    #testNum=1
    #splitProportion=0.2
    
    allFeaturesF1=[]
    allFeaturesRecall=[]
    allFeaturesPrecision=[]
    
    featureSelctedF1=[]
    featureSelctedRecall = []
    featureSelctedPrecision = []
    
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
            
            #clf = RandomForestClassifier()#criterion='entropy')
            #clf = tree.DecisionTreeClassifier()#max_depth=p)
            clf = AdaBoostClassifier()
            #clf = GradientBoostingClassifier()#, learning_rate=lr)
            #clf = ExtraTreesClassifier(n_estimators=p)
                        
            #svc = LinearSVC()
            #selector = RFE(estimator=svc, n_features_to_select=p*19, step=0.2)
            selector = SelectPercentile(chooser, percentile=p)
            
            selector.fit(X, y)
            name = str(clf).split()[0].split('(')[0]
            clf.fit(selector.transform(X), y)
            pred = clf.predict(selector.transform(X_test))
            
            featureSelctedF1.append(metrics.f1_score(y_test, pred))
            featureSelctedRecall.append(metrics.recall_score(y_test, pred))
            featureSelctedPrecision.append(metrics.precision_score(y_test, pred)) 
            
            clf.fit(X, y)
            pred = clf.predict(X_test)
            
            allFeaturesF1.append(metrics.f1_score(y_test, pred))
            allFeaturesRecall.append(metrics.recall_score(y_test, pred))
            allFeaturesPrecision.append(metrics.precision_score(y_test, pred))

    return np.mean(allFeaturesF1), np.mean(featureSelctedF1), \
        np.mean(allFeaturesRecall), np.mean(featureSelctedRecall), \
        np.mean(allFeaturesPrecision), np.mean(featureSelctedPrecision), \
        name

"""
ds = labanUtil.getPybrainDataSet('Rachelle')
print ds.getLength()
print len(ds.getSample(0)[0])
print eval(ds, 20)

"""
if __name__ == '__main__':
    qualities, combinations = cp.getCombinations()
    pool = Pool(6)  
    source = 'Rachelle' 
    ds = labanUtil.getPybrainDataSet(source)
    #print 'input diamention: ', len(ds.getSample(0)[0])
    inLayerSize = len(ds.getSample(0)[0])
    outLayerSize = len(ds.getSample(0)[1])
    
    allFeaturesF1=[]
    allFeaturesRecall=[]
    allFeaturesPrecision=[]
    
    featureSelctedF1=[]
    featureSelctedRecall = []
    featureSelctedPrecision = []

    #params = np.linspace(0.1, 1, 10)
    params = [2,3,4,5,6,7]
    m = {}
    splitProportion=0.2
    testNum=100
    for i,p in enumerate(params):
        m[i] = pool.apply_async(eval, [ds, testNum, p, splitProportion])
    for i,nEstimators in enumerate(params):
        aF1, fsF1, aRecall, fsRecall, aPrecision, fsPrecision, name = m[i].get()
        
        allFeaturesF1.append(aF1)
        allFeaturesRecall.append(aRecall)
        allFeaturesPrecision.append(aPrecision)
        
        featureSelctedF1.append(fsF1)
        featureSelctedRecall.append(fsRecall)
        featureSelctedPrecision.append(fsPrecision)
        
    #print 'max of featureSelctedF1: ', m
    #print 'Avarage of all: ', av

    dsSize = ds.getLength()
    vecLen = len(ds.getSample(0)[0])
    
    def plotRes(allFeatures, featureSelcted, metric):
        m = np.max(featureSelcted)
        av = np.mean(allFeatures)
        plt.figure()
        #plt.plot(params, allFeatures, label='All the features, average: '+str(av))
        dif = np.array(featureSelcted) - np.array(allFeatures)
        plt.plot(params,dif, label=chooser.__name__+', max: '+ str(m))
        plt.legend().draggable()
        plt.xlabel('Number of features (as aprecent from the original vector)')
        plt.ylabel('Difference in ' + metric+' score')
        plt.title('Metric: '+metric+', CLF: '+name+', CMA: '+source+ \
                  ', DS size: '+str(dsSize)+ ', Vector size: '+str(vecLen)+ \
                  ', Split prop: '+str(splitProportion)+', Repeated: '+str(testNum)\
                  +', All the features, average: '+str(av))
    plotRes(allFeaturesF1, featureSelctedF1, 'F1')
    plotRes(allFeaturesRecall, featureSelctedRecall, 'Recall')
    plotRes(allFeaturesPrecision, featureSelctedPrecision, 'Precision')
    plt.show()










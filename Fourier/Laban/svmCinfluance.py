import numpy as np
import LabanUtils.util as labanUtil
import LabanUtils.combinationsParser as cp
import Laban.algorithm.generalExtractor as ge
import matplotlib.pyplot as plt
from sklearn import metrics, svm
from sklearn.svm import LinearSVC
from sklearn.ensemble import AdaBoostClassifier, RandomForestClassifier
from sklearn.ensemble import GradientBoostingClassifier
from multiprocessing import Pool
import math
from sklearn.feature_selection import f_classif, SelectKBest, f_regression,RFECV
from sklearn.pipeline import Pipeline
import LabanUtils.informationGain as ig
import matplotlib

chooser=f_classif#ig.recursiveRanking#ig.infoGain##
    #splitProportion = 0.2
import mlpy
CMAs = ['Rachelle', 'Karen']
trainSource = CMAs[0]
testSource = CMAs[1]
withPCA=False
fs=False
#clf = AdaBoostClassifier()
#clf = svm.SVC(C=c, class_weight={1: ratio}, kernel='rbf')

tstdata, featuresNames = labanUtil.getPybrainDataSet(testSource)  
trndata, _ = labanUtil.getPybrainDataSet(trainSource)  
print 'Datasets were read'
X, Y = labanUtil.fromDStoXY(trndata)
X_test, Y_test = labanUtil.fromDStoXY(tstdata)

bestFeatures = open('bestFeatures.csv', 'w')
bestFeatures.flush()
bestFeatures.write('Quality, Feature Name, Operator, F-value, p-value\n')

performance = open('performance.csv', 'w')
performance.flush()
performance.write('Quality, Precision, Recall, F1 score\n')
totalF1Train=[]
totalF1Test=[]
totalPrecisionTest=[]
totalRecallTest=[]
totalCoesfs = []
cs = np.logspace(-3, 5, 40)
#cws = range(1,20)
for c in cs:
#for ratio in cws:
    #c=80
    ratio =5
    percentile=5
    clf = svm.LinearSVC(C=c,  loss='LR', penalty='L1', dual=False, class_weight='auto')#{1: ratio})
    f1sTrain = []
    f1s=[]
    ps =[]
    rs=[]
    ls = []
    qualities, combinations = cp.getCombinations()
    selectedFeaturesNum = 25
    for i, (y, y_test) in enumerate(zip(Y, Y_test)):
        if all(v == 0 for v in y):
            continue
        anova_filter = SelectKBest(chooser, k=selectedFeaturesNum)
        pipe = Pipeline([
                        ('feature_selection', anova_filter),
                        ('classification', clf)
                        ])
        pipe.fit(X, y)
        #print clf.coef_
        coefs = clf.coef_[0]
        #print coefs
        l = len([c for c in coefs if c!=0])
        ls.append(l)
        #print l
        #print clf.classes_
        predTrain =  pipe.predict(X)
        f1sTrain.append(metrics.f1_score(y, predTrain))
        
        pred = pipe.predict(X_test)
        precision = metrics.precision_score(y_test, pred)
        recall = metrics.recall_score(y_test, pred)
        #f1 = metrics.f1_score(y_test, pred, average=None)[1]
        if (precision + recall) == 0:
            f1 = 0
        else:
            f1= 2*precision*recall/(precision + recall)
        performance.write(qualities[i]+', '+ str(round(precision,3))\
                          +', '+ str(round(recall,3))\
                          +', '+ str(round(f1, 3))+'\n')
                          
        f1s.append(f1)
        ps.append(precision)
        rs.append(recall)
        name = str(clf).split()[0].split('(')[0]
    totalF1Test.append(np.mean(f1s))
    totalPrecisionTest.append(np.mean(ps))
    totalRecallTest.append(np.mean(rs))
    totalF1Train.append(np.mean(f1sTrain))
    totalCoesfs.append(np.mean(ls))
bestFeatures.close()
performance.close()
ax = plt.subplot()
print zip(totalPrecisionTest, totalRecallTest,totalF1Test)
ax.plot(cs, totalF1Test, label='Test F1')
ax.plot(cs, totalPrecisionTest, label='Test Precision')
ax.plot(cs, totalRecallTest, label='Test Recall')
ax.plot(cs, totalF1Train, label='Train F1')
ax.legend().draggable()
ax.set_xscale("log", nonposx='clip')
trainSize = trndata.getLength()
testSize = tstdata.getLength()
vecLen = len(trndata.getSample(0)[0])
name = str(clf).split()[0].split('(')[0]
testedParam = 'C'
plt.title('Tested param: '+testedParam \
         + ', CLF: '+name \
         + '\n Train set: CMA #1'+' size-'+str(trainSize) \
         + ', Test set: CMA #2'+' size-'+str(testSize) \
         + ', Features num: '+str(vecLen) \
         + '\n Featue selection (FS) method: '+chooser.__name__ \
         + ', Features num after FS: '+str(selectedFeaturesNum) \
         #+', chopFactor: '+str(ge.chopFactor)
         #+', with PCA: ' +str(withPCA)
         #+', with fs: ' +str(fs)
         +', cw: '+str(ratio))

plt.xlabel(testedParam)
plt.ylabel('Performance')
plt.figure()
ax = plt.subplot()
ax.plot(cs, totalCoesfs)
ax.set_xscale("log", nonposx='clip')
plt.title('C influence on classifier sparsity')
plt.xlabel('C')
plt.ylabel('Number of coefs')
plt.show()


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

chooser=ig.infoGain#f_classif#ig.recursiveRanking#
    #splitProportion = 0.2
import mlpy
CMAs = ['Rachelle', 'Karen']
trainSource = CMAs[0]
testSource = CMAs[1]
withPCA=False
fs=False
c=80
selectedFeaturesNum = 25
ratio ='auto'
#percentile=5
clf = svm.LinearSVC(C=c,  loss='LR', penalty='L1', dual=False, class_weight='auto')#{1: ratio})
#clf = AdaBoostClassifier()
#clf = svm.SVC(C=c, class_weight={1: ratio}, kernel='rbf')

tstdata, featuresNames = labanUtil.getPybrainDataSet(testSource)  
trndata, _ = labanUtil.getPybrainDataSet(trainSource)  
print 'Data was read'
X, Y = labanUtil.fromDStoXY(trndata)
X_test, Y_test = labanUtil.fromDStoXY(tstdata)
f1s=[]
ps =[]
rs=[]

bestFeatures = open('bestFeatures.csv', 'w')
bestFeatures.flush()
bestFeatures.write('Quality, Feature Name, Operator, Information Gain, p-value\n')

performance = open('performance.csv', 'w')
performance.flush()
performance.write('Quality, Precision, Recall, F1 score, Train F1 Score, Active Features amount \n')

qualities, combinations = cp.getCombinations()

for i, (y, y_test) in enumerate(zip(Y, Y_test)):
    print qualities[i]
    if all(v == 0 for v in y):
        continue
    """
    
    #selector = SelectPercentile(chooser, percentile=percentile)
    """
    """
    pca = mlpy.PCA()
    pca.learn(np.array(X))
    withPCA=True
    X = pca.transform(X)
    X_test = pca.transform(X_test)
    """
    """
    selector = RFECV(clf, step=0.01)
    selector = selector.fit(X, y)
    #print len([x for x in selector.support_ if x==True])
    chooser = RFECV
    pred = selector.predict(X_test)
    """
    anova_filter = SelectKBest(chooser, k=selectedFeaturesNum)
    pipe = Pipeline([
                    ('feature_selection', anova_filter),
                    ('classification', clf)
                    ])
    pipe.fit(X, y)
    
    coefs = clf.coef_[0]
    activeCoefsNum = len([c for c in coefs if c!=0])
    
    predTrain =  pipe.predict(X)
    f1sTrain = metrics.f1_score(y, predTrain)
    #print len([c for c in clf.coef_ if c != 0])
    pred = pipe.predict(X_test)
    
    precision = metrics.precision_score(y_test, pred)
    recall = metrics.recall_score(y_test, pred)
    f1 = metrics.f1_score(y_test, pred)
    performance.write(qualities[i]
                      +', '+ str(round(precision,3))\
                      +', '+ str(round(recall,3))\
                      +', '+ str(round(f1, 3))\
                      +', '+ str(round(f1sTrain, 3))\
                      +', '+ str(activeCoefsNum)\
                      +'\n')
    
    
    selector = SelectKBest(chooser, 1)
    selector.fit(X, y)
    featureNum = selector.get_support().tolist().index(True)
    pstr = str(selector.pvalues_[featureNum])
    pstr = pstr[:3] + pstr[-4:]
    scoreStr = str(round(selector.scores_[featureNum],2))
    bestFeatures.write(qualities[i]+', '+ featuresNames[featureNum]+\
                       ', '+scoreStr+', ' +pstr+ '\n')                  
    f1s.append(f1)
    ps.append(precision)
    rs.append(recall)
    name = str(clf).split()[0].split('(')[0]
bestFeatures.close()
performance.close()


m = np.mean(f1s)
print m, ge.chopFactor
fig, ax = plt.subplots()
ind = np.arange(len(qualities))
width = 0.25   
f1Rects = ax.bar(ind, f1s, width, color='g', label='F1: '+str(round(np.mean(f1s),3)) )
pRecrs = ax.bar(ind+width, ps, width, color='b', label='Precision: '+str(round(np.mean(ps),3)))
rRects = ax.bar(ind-width, rs, width, color='r', label='Recall: '+str(round(np.mean(rs),3)))
ax.set_xticks(ind)
#ax.set_xticklabels(ind)
xtickNames = plt.setp(ax, xticklabels=qualities)
plt.setp(xtickNames, rotation=90)#, fontsize=8)
ax.set_xticklabels(qualities)
"""
def autolabel(rects):
    # attach some text labels
    for i,rect in enumerate(rects):
        height = rect.get_height()
        ax.text(rect.get_x()+rect.get_width()/2., 1.05*height, qualities[i],#'%d'%int(height),
                ha='center', va='bottom')
autolabel(f1Rects)
"""
ax.legend().draggable()
trainSize = trndata.getLength()
testSize = tstdata.getLength()
vecLen = len(trndata.getSample(0)[0])
name = str(clf).split()[0].split('(')[0]
#plt.title('F1 mean: '+str(m)+', Test amount: '+str(testNum))
font = {'family' : 'normal',
        'style' : 'italic',
        'size'   : 20}
#legend([plot1], "title", prop = font)
matplotlib.rc('font', **font)

plt.title('CLF: '+name \
         + ', Train set: CMA #1'+' size-'+str(trainSize) \
         + ', Test set: CMA #2'+' size-'+str(testSize) \
         + '\n Features num: '+str(vecLen) \
         + ', Featue selection (FS) method: '+chooser.__name__ \
         + ', Features num after FS: '+str(selectedFeaturesNum) \
         #+', chopFactor: '+str(ge.chopFactor)
         #+', with PCA: ' +str(withPCA)
         #+', with fs: ' +str(fs)
         +'\n with C: ' +str(c)
         +', cw: '+str(ratio))
plt.xlabel('Quality')
plt.ylabel('F1 score')
plt.show()

import numpy as np
import LabanUtils.util as labanUtil
import LabanUtils.combinationsParser as cp
import matplotlib.pyplot as plt
from sklearn import metrics, svm
from sklearn.svm import SVR
from sklearn.ensemble import AdaBoostClassifier
from sklearn.ensemble import GradientBoostingClassifier
from multiprocessing import Pool
import math
from sklearn.feature_selection import SelectPercentile, f_classif, \
    f_oneway, f_regression, chi2, RFE, RFECV 

chooser=f_regression
def eval(ds, clf, splitProportion=0.2, p=4):
    #splitProportion = 0.2
    import numpy as np
import LabanUtils.util as labanUtil
import LabanUtils.combinationsParser as cp
import matplotlib.pyplot as plt
from sklearn import metrics, svm
from sklearn.svm import SVR
from sklearn.ensemble import AdaBoostClassifier
from sklearn.ensemble import GradientBoostingClassifier
from multiprocessing import Pool
import math
from sklearn.feature_selection import SelectPercentile, f_classif, \
    f_oneway, f_regression, chi2, RFE, RFECV 

    #splitProportion = 0.2

tstdata = labanUtil.getPybrainDataSet('Karen')  
trndata = labanUtil.getPybrainDataSet('Rachelle')  
print 'trndata '+str(len(trndata.getSample(0)[0]))
print 'tstdata '+str(len(tstdata.getSample(0)[0]))
X, Y = labanUtil.fromDStoXY(trndata)
X_test, Y_test = labanUtil.fromDStoXY(tstdata)
f1s=[]
ps =[]
rs=[]
clf = AdaBoostClassifier()
percentile=5
for i, (y, y_test) in enumerate(zip(Y, Y_test)):
    if all(v == 0 for v in y):
        continue
    
    """
    es = SVR(kernel='linear')
    clf = RFECV(estimator=es, step=0.05)
    clf.fit(X, y)
    pred = clf.predict(X_test)
    """
    
    selector = SelectPercentile(chooser, percentile=percentile)
    selector.fit(X, y)
    name = str(clf).split()[0].split('(')[0]
    clf.fit(selector.transform(X), y)
    pred = clf.predict(selector.transform(X_test))
    f1 = metrics.f1_score(y_test, pred)
    f1s.append(f1)
    ps.append(metrics.precision_score(y_test, pred))
    rs.append(metrics.recall_score(y_test, pred))


qualities, combinations = cp.getCombinations()

m = np.mean(f1s)
print m
print f1s
fig, ax = plt.subplots()
ind = np.arange(len(qualities))
width = 0.25   
f1Rects = ax.bar(ind, f1s, width, color='g', label='f1: '+str(np.mean(f1s)) )
pRecrs = ax.bar(ind+width, ps, width, color='b', label='precision: '+str(np.mean(ps)))
rRects = ax.bar(ind+2*width, rs, width, color='r', label='recall: '+str(np.mean(rs)))
ax.set_xticks(ind+width)
ax.set_xticklabels(ind)
def autolabel(rects):
    # attach some text labels
    for i,rect in enumerate(rects):
        height = rect.get_height()
        ax.text(rect.get_x()+rect.get_width()/2., 1.05*height, qualities[i],#'%d'%int(height),
                ha='center', va='bottom')
autolabel(f1Rects)
ax.legend().draggable()
trainSize = trndata.getLength()
testSize = tstdata.getLength()
vecLen = len(trndata.getSample(0)[0])
name = str(clf).split()[0].split('(')[0]
#plt.title('F1 mean: '+str(m)+', Test amount: '+str(testNum))
plt.title('CLF: '+name+'Featue selection: '+chooser.__name__ + \
          ', percentile: '+str(percentile)\
         + ', Train set size: '+str(trainSize) \
         + ', Split prop: ' +str(testSize)+ ', Vector size: '+str(vecLen) )
plt.xlabel('Quality index')
plt.ylabel('F1 score')
plt.show()

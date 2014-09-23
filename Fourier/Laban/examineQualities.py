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
    f_oneway, f_regression, chi2, SelectKBest
from sklearn.pipeline import Pipeline

import matplotlib

#from matplotlib.font_manager import FontProperties
#fontP = FontProperties()
#fontP.set_size('small')
font = {'family' : 'normal',
        'style' : 'italic',
        'size'   : 18}
#legend([plot1], "title", prop = font)
matplotlib.rc('font', **font)

chooser=f_classif
selectedFeaturesNum=50

def eval(ds, clf, splitProportion=0.2, p=4):
    #splitProportion = 0.2
    tstdata, trndata = ds.splitWithProportion( splitProportion )
    X, Y = labanUtil.fromDStoXY(trndata)
    X_test, Y_test = labanUtil.fromDStoXY(tstdata)
    f1s=[]
    ps =[]
    rs=[]
    for i, (y, y_test) in enumerate(zip(Y, Y_test)):
        anova_filter = SelectKBest(f_classif, k=selectedFeaturesNum)
        pipe = Pipeline([
                        ('feature_selection', anova_filter),
                        ('classification', clf)
                        ])
        pipe.fit(X, y)
        pred = pipe.predict(X_test)
        name = str(clf).split()[0].split('(')[0]
        #clf.fit(selector.transform(X), y)
        #pred = clf.predict(selector.transform(X_test))
        f1 = metrics.f1_score(y_test, pred)
        f1s.append(f1)
        ps.append(metrics.precision_score(y_test, pred))
        rs.append(metrics.recall_score(y_test, pred))
    return f1s, ps, rs

if __name__ == '__main__':
    p = Pool(8)
    qualities, combinations = cp.getCombinations()
    source = 'Rachelle' 
    ds, featuresNames = labanUtil.getPybrainDataSet(source)
    inLayerSize = len(ds.getSample(0)[0])
    outLayerSize = len(ds.getSample(0)[1])
    f1s = []
    ps=[] 
    rs=[]
    testNum=24
    for _ in qualities:
        f1s.append([])
        ps.append([])
        rs.append([])
    m = {}
    clf = AdaBoostClassifier()
    splitProportion=0.2
    percentile=5
    for i in range(testNum):
        m[i] = p.apply_async(eval, [ds, clf, splitProportion])
    for i in range(testNum):
        cf1s, cps, crs = m[i].get()
        for i,(f,p,r) in enumerate(zip(cf1s, cps, crs)):
            f1s[i].append(f)
            ps[i].append(p)
            rs[i].append(r)
    for i,_ in enumerate(qualities):
        f1s[i] = np.mean(f1s[i])
        ps[i]=np.mean(ps[i])
        rs[i]=np.mean(rs[i])
        
    m = np.mean(f1s)
    print m
    print f1s
    fig, ax = plt.subplots()
    ind = np.arange(len(qualities))
    width = 0.25   
    f1Rects = ax.bar(ind, f1s, width, color='g', label='F1: '+str(round(np.mean(f1s),3)) )
    pRecrs = ax.bar(ind+width, ps, width, color='b', label='Precision: '+str(round(np.mean(ps),3)))
    rRects = ax.bar(ind-width, rs, width, color='r', label='Recall: '+str(round(np.mean(rs),3)))
    ax.set_xticks(ind+width)
    xtickNames = plt.setp(ax, xticklabels=qualities)
    plt.setp(xtickNames, rotation=60)#, fontsize=8)
    ax.set_xticklabels(qualities)
    """
    def autolabel(rects):
        # attach some text labels
        for i,rect in enumerate(rects):
            height = rect.get_height()
            #ax.text(rect.get_x()+rect.get_width()/2., 1.05*height, qualities[i],#'%d'%int(height),
             #       ha='center', va='bottom')
    autolabel(f1Rects)
    """
    ax.legend().draggable()
    dsSize = ds.getLength()
    vecLen = len(ds.getSample(0)[0])
    name = str(clf).split()[0].split('(')[0]
    #plt.title('F1 mean: '+str(m)+', Test amount: '+str(testNum))
    plt.title('CLF: '+name+
              ', Featue selection: '+chooser.__name__  
              #+ ', percentile: '+str(percentile) 
              #+ ', CMA: ' + source
              + ',\n Dataset size: '+str(dsSize) 
              + ', Original number of features: ' + str(vecLen)
              + ', \nNumber of features after selection: '+str(selectedFeaturesNum)
              + ', Split prop: ' +str(splitProportion)
              + ', Repetition number: '+str(testNum))
    plt.xlabel('Quality')
    #plt.xticks(*enumerate(qualities))
    plt.ylabel('Performance')
    plt.ylim((0,1.2))
    #xtickNames = plt.setp(ax1, xticklabels=qualities)
    #plt.setp(xtickNames, rotation=45, fontsize=8)
    
    plt.show()











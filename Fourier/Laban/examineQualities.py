import numpy as np
import LabanUtils.util as labanUtil
import LabanUtils.combinationsParser as cp
import matplotlib.pyplot as plt
from sklearn import metrics
from sklearn.ensemble import AdaBoostClassifier
from sklearn.ensemble import GradientBoostingClassifier
from multiprocessing import Pool
import math

def eval(ds):
    splitProportion = 0.2
    tstdata, trndata = ds.splitWithProportion( splitProportion )
    X, Y = labanUtil.fromDStoXY(trndata)
    X_test, Y_test = labanUtil.fromDStoXY(tstdata)
    f1s=[]
    ps =[]
    rs=[]
    for i, (y, y_test) in enumerate(zip(Y, Y_test)):
        if all(v == 0 for v in y):
            continue
        clf = GradientBoostingClassifier()
        #name = str(clf).split()[0].split('(')[0]
        clf.fit(X, y)
        pred = clf.predict(X_test)
        f1 = metrics.f1_score(y_test, pred)
        f1s.append(f1)
        ps.append(metrics.precision_score(y_test, pred))
        rs.append(metrics.recall_score(y_test, pred))
    return f1s, ps, rs

if __name__ == '__main__':
    p = Pool(7)
    qualities, combinations = cp.getCombinations()
    print len(qualities)
    
    ds = labanUtil.getPybrainDataSet()
    inLayerSize = len(ds.getSample(0)[0])
    outLayerSize = len(ds.getSample(0)[1])
    f1s = []
    ps=[] 
    rs=[]
    testNum=100
    for _ in qualities:
        f1s.append([])
        ps.append([])
        rs.append([])
    m = {}
    for i in range(testNum):
        m[i] = p.apply_async(eval, [ds])
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
    f1Rects = ax.bar(ind, f1s, width, color='g', label='f1')
    pRecrs = ax.bar(ind+width, ps, width, color='b', label='precision')
    rRects = ax.bar(ind+2*width, rs, width, color='r', label='recall')
    ax.set_xticks(ind+width)
    ax.set_xticklabels(ind)
    def autolabel(rects):
        # attach some text labels
        for i,rect in enumerate(rects):
            height = rect.get_height()
            ax.text(rect.get_x()+rect.get_width()/2., 1.05*height, qualities[i],#'%d'%int(height),
                    ha='center', va='bottom')
    autolabel(f1Rects)
    ax.legend()#(f1Rects[0], pRecrs[0], rRects[0]), ('f1', 'precision', 'recall'))
    plt.title('F1 score for every quality, mean: '+str(m)+', test amount: '+str(testNum))
    plt.xlabel('Quality index')
    plt.ylabel('F1 score')
    plt.show()











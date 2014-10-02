from sklearn import lda
import LabanUtils.util as labanUtil
import matplotlib.pyplot as plt
import pylab as pl

import numpy as np
from sklearn import svm
from sklearn.feature_selection import SelectKBest, f_classif
from sklearn.pipeline import Pipeline
import LabanUtils.combinationsParser as cp
from sklearn import (manifold, datasets, decomposition, ensemble, lda,
                     random_projection)

quality = 'Advance'
trainSource = 'Karen'
testSource = 'Rachelle'
trndata, featuresNames = labanUtil.getPybrainDataSet(trainSource)  
#tstdata, featuresNames = labanUtil.getPybrainDataSet(trainSource)  
#X_test, Y_test = labanUtil.fromDStoXY(tstdata)
X, Y = labanUtil.fromDStoXY(trndata)
qualities, combinations = cp.getCombinations()
y=Y[qualities.index('Strong')]

c=80
selectedFeaturesNum = 25
ratio ='auto'
clf = svm.LinearSVC(C=c,  loss='LR', penalty='L1', dual=False, class_weight='auto')#{1: ratio})
chooser=f_classif#ig.infoGain#ig.recursiveRanking
anova_filter = SelectKBest(chooser, k=selectedFeaturesNum)
pipe = Pipeline([
                ('feature_selection', anova_filter),
                ('classification', clf)
                ])
pipe.fit(X, y)

coefs = np.array(clf.coef_[0])
activeCoefsIndices = np.nonzero(coefs)[0]
X_svm = X[:,activeCoefsIndices]

#X_transformed = lda.LDA(n_components=3).fit_transform(X, y)
#embedder =  manifold.SpectralEmbedding(n_components=2, random_state=0,
#                                      eigen_solver="arpack")
#embedder = manifold.TSNE(n_components=2, init='pca', random_state=0)
#X_transformed = embedder.fit_transform(X)
X_transformed=X_svm
def cor(x01, x02):
    return max(np.correlate(x01,x02))/np.sqrt(np.dot(x01,x01)*np.dot(x02,x02))

#if np.abs(cor(X_transformed[:,0], X_transformed[:,1]))
print cor(X_transformed[:,0], X_transformed[:,1])
"""
for i,tag in enumerate(y):
    color = 'red' if tag else 'blue'
    plt.scatter(X_transformed[i,0],X_transformed[i,1], c=color) 
plt.show()
"""

xx = np.linspace(-1, 5, 10)
yy = np.linspace(-1, 5, 10)

X1, X2 = np.meshgrid(xx, yy)
Z = np.empty(X1.shape)
for (i, j), val in np.ndenumerate(X1):
    x1 = val
    x2 = X2[i, j]
    p = clf.decision_function([x1, x2])
    Z[i, j] = p[0]
levels = [-1.0, 0.0, 1.0]
linestyles = ['dashed', 'solid', 'dashed']
colors = 'k'
pl.contour(X1, X2, Z, levels, colors=colors, linestyles=linestyles)
pl.scatter(X[:, 0], X[:, 1], c=Y, cmap=pl.cm.Paired)

pl.axis('tight')
pl.show()
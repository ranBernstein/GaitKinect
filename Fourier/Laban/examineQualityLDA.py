from sklearn import lda
import LabanUtils.util as labanUtil
import matplotlib.pyplot as plt
import pylab as pl
from sklearn.linear_model import SGDClassifier

import numpy as np
from sklearn import svm
from sklearn.feature_selection import SelectKBest, f_classif
from sklearn.pipeline import Pipeline
import LabanUtils.combinationsParser as cp
from sklearn import manifold, datasets, decomposition, ensemble, lda, random_projection

quality = 'Advance'
trainSource = 'Karen'
testSource = 'Rachelle'
trndata, featuresNames = labanUtil.getPybrainDataSet(trainSource)  
#tstdata, featuresNames = labanUtil.getPybrainDataSet(trainSource)  
#X_test, Y_test = labanUtil.fromDStoXY(tstdata)
X, Y = labanUtil.fromDStoXY(trndata)
qualities, combinations = cp.getCombinations()
y=Y[qualities.index(quality)]

"""
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
"""
for i,tag in enumerate(y):
    color = 'red' if tag else 'blue'
    plt.scatter(X_transformed[i,0],X_transformed[i,1], c=color) 
plt.show()
"""

xx = np.linspace(-10000,25000, 10)
yy = np.linspace(-10000,25000, 10)


tnse = manifold.TSNE(n_components=2, init='pca', random_state=0)
X = tnse.fit_transform(X)
print X.shape
clf = SGDClassifier(loss="hinge", alpha=0.01, n_iter=200, fit_intercept=True)
clf.fit(X, y)

X1, X2 = np.meshgrid(xx, yy)
Z = np.empty(X1.shape)
for (i, j), val in np.ndenumerate(X1):
    x1 = val
    x2 = X2[i, j]
    p = clf.decision_function([x1, x2])
    Z[i, j] = p[0]
print Z
levels = [-10000.0, 0.0, 10000.0]
linestyles = ['dashed', 'solid', 'dashed']
colors = 'k'
pl.contour(X1, X2, Z, levels, colors=colors, linestyles=linestyles)
for x, tag in zip(X, y):
    color = 'red' if tag else 'blue'
    pl.scatter(x[0], x[1], c=color)

pl.axis('tight')
pl.title(quality)
pl.show()
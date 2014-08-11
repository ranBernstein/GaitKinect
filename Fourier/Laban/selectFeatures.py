import numpy as np
import pylab as pl
from sklearn import datasets, svm
from sklearn.feature_selection import SelectPercentile, f_classif
import LabanUtils.util as labanUtil
import LabanUtils.combinationsParser as cp
from multiprocessing import Pool

ds = labanUtil.getPybrainDataSet()
X, Y = labanUtil.fromDStoXY(ds)
X, Y = np.array(X), np.array(Y)



X_indices = np.arange(X.shape[-1])

###############################################################################
# Univariate feature selection with F-test for feature scoring
# We use the default selection function: the 10% most significant features
selector = SelectPercentile(f_classif, percentile=10)
selector.
selector.fit(X, Y[0])
scores = -np.log10(selector.pvalues_)
#scores /= scores.max()
pl.bar(X_indices - .45, scores, width=.2,
       label=r'Univariate score ($-Log(p_{value})$)', color='g')
###############################################################################
# Compare to the weights of an SVM
clf = svm.SVC(kernel='linear')
clf.fit(X, y)

svm_weights = (clf.coef_ ** 2).sum(axis=0)
svm_weights /= svm_weights.max()

pl.bar(X_indices - .25, svm_weights, width=.2, label='SVM weight', color='r')
"""

clf_selected = svm.SVC(kernel='linear')
clf_selected.fit(selector.transform(X), y)

svm_weights_selected = (clf_selected.coef_ ** 2).sum(axis=0)
svm_weights_selected /= svm_weights_selected.max()

pl.bar(X_indices[selector.get_support()] - .05, svm_weights_selected, width=.2,
       label='SVM weights after selection', color='b')


pl.title("Comparing feature selection")
pl.xlabel('Feature number')
pl.yticks(())
pl.axis('tight')
pl.legend(loc='upper right')
"""
pl.show()
from sklearn.tree import DecisionTreeClassifier, export_graphviz
import numpy as np
import Laban.LabanUtils.util as labanUtil
from StringIO import StringIO
import pydot
    
def infoGain(X, y):
    X = np.array(X)
    clf = DecisionTreeClassifier(criterion='entropy')
    clf.fit(X,y)
    importances = clf.tree_.compute_feature_importances()
    return importances

def bestByInfoGain(X, y, featuresNames):
    importances = infoGain(X, y)
    bestFeatureName = featuresNames[np.argmax(importances)]
    return max(importances), bestFeatureName

def createDiagram(X, y, featuresNames, fileName='out.pdf'):
    X = np.array(X)
    clf = DecisionTreeClassifier(criterion='entropy')
    clf.fit(X,y)
    out = StringIO()
    out = export_graphviz(clf, out_file=out)
    value = out.getvalue()
    graph = pydot.graph_from_dot_data(value) 
    graph.write_pdf(fileName+'.pdf') 


"""
trainSource = 'Karen'
trndata, featuresNames = labanUtil.getPybrainDataSet(trainSource)  
X, Y = labanUtil.fromDStoXY(trndata)
y=Y[0]
X, y = [[1,1,0], [1,0,0], [0,0,0]], [1,0,1]
print bestInfoGain(X, y, ['a','b'])
"""


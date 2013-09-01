import numpy as np
from sklearn import datasets
from amcParser import getMergedData
import time
from sklearn import tree
from sklearn.neighbors import KNeighborsClassifier
from sklearn import svm
from sklearn.ensemble import GradientBoostingClassifier

clf = GradientBoostingClassifier(n_estimators=100, learning_rate=1.0, max_depth=4, random_state=0)

#clf = svm.SVC()

#clf = tree.DecisionTreeClassifier()

#clf = KNeighborsClassifier()
#clf.n_neighbors = 5
#clf.weights = 'distance' 


def crossValidate(data, tags, trainSize):  
    fit = clf.fit(dataTrain, tagTrain)
    
    return clf.score(dataTest, tagsTest)
    
    res = clf.predict(dataTest)
    hits = 0.0
    for t,r in zip(tagsTest,res):
        if(t==r):
            hits+=1.0
    return hits/float(len(res))

sum = 0.0
numOftests = 50
joints = np.array(['cycle_duration','lradius', 'rradius', 'ltibia', 'rtibia', 'lwrist', 'rwrist', 'lfingers', 'rfingers'])
chosen = np.array([0,1,1,0,0,0,0,0,0])
data, tags = getMergedData(joints[chosen.astype(np.bool)])
numOfsamples, numOfFeatures = data.shape
print(joints[chosen.astype(np.bool)]) 
trainSize = numOfsamples-1#int(0.9*numOfsamples)    
for i in range(numOftests):
    np.random.seed(i)
    indices = np.random.permutation(len(data))
    dataTrain = data[indices[:trainSize]]
    tagTrain = tags[indices[:trainSize]]
    dataTest  = data[indices[trainSize:]]
    tagsTest  = tags[indices[trainSize:]]
    sum += crossValidate(data, tags, trainSize)
print(sum/float(numOftests))
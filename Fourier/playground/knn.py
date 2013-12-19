import numpy as np
from sklearn import datasets
from sklearn.neighbors import KNeighborsClassifier
from utils.amcParser import getMergedData
import time

knn = KNeighborsClassifier()
knn.n_neighbors = 5
knn.weights = 'distance' 

def crossValidate(data, tags, trainSize):  
    fit = knn.fit(dataTrain, tagTrain)
    #print(fit)
    res = knn.predict(dataTest)
    hits = 0.0
    for t,r in zip(tagsTest,res):
        if(t==r):
            hits+=1.0
    #print(res)
    #print(tagsTest)
    return hits/float(len(res))

sum = 0.0
numOftests = 100
for i in range(numOftests):
    joints = np.array(['lradius', 'rradius', 'ltibia', 'rtibia', 'lwrist', 'rwrist', 'lfingers', 'rfingers'])
    chosen = np.array([1,1,1,0,0,0,1,1])
    data, tags = getMergedData(joints[chosen.astype(np.bool)])
    numOfsamples, numOfFeatures = data.shape
    np.random.seed(i)
    trainSize = numOfsamples-1#int(0.9*numOfsamples)    
    indices = np.random.permutation(len(data))
    dataTrain = data[indices[:trainSize]]
    tagTrain = tags[indices[:trainSize]]
    dataTest  = data[indices[trainSize:]]
    tagsTest  = tags[indices[trainSize:]]
    sum += crossValidate(data, tags, trainSize)
print(sum/float(numOftests))
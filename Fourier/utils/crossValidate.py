import numpy as np
import random

def crossValidate(cl, data, tags, testSize, testAmount):
    hits=0.0
    counter = 0.0
    testFactors = np.linspace(0.03, 0.97, 20)
    scores = []
    clfs = []
    for j in xrange(testAmount):
        testIndices = random.sample(set(xrange(len(data))), testSize)
        trainData = []
        trainTags = []
        dataTest = []
        tagsTest = []
        for i in xrange(len(data)):
            if i in testIndices:
                dataTest.append(data[i]) 
                tagsTest.append(tags[i])
            else:
                trainData.append(data[i])
                trainTags.append(tags[i])
        
        fit = cl.fit(trainData, trainTags)
        res = cl.predict(dataTest)
        for i in xrange(testSize):
            if(res[i] == tagsTest[i]):
                hits+=1
            counter+=1
            i+=1
    score = hits/counter*100
    return score
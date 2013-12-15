from amcParser import getAMCperiod
from periodAnalysisUtils import alignByMax
import matplotlib.pyplot as plt
import math
import numpy as np
import interpulation
from sklearn import datasets
from sklearn.neighbors import KNeighborsClassifier
import random
import copy
import gc

numOfFeatures = 100
subjects = [8, 16, 35 ,39]
frameSize = math.ceil(np.sqrt(len(subjects)))
fig = plt.figure()
joint = 'rtibia'
plt.xlabel('Time (in frames)')
plt.ylabel(joint + ' angle')
fig_uniform = plt.figure()
data = []
tags = []
for subject in subjects:
    for stride in xrange(1,13):
        file = 'AMCs/subjects/' + str(subject) + '/' + str(stride) + '.amc'
        try:
            input = getAMCperiod(joint, file)
        except:
            continue
        input = alignByMax(input)
        sub =  fig.add_subplot(frameSize*110 + subjects.index(subject))
        sub.plot(range(len(input)), input)
        sub_uniform = fig_uniform.add_subplot(frameSize*110 + subjects.index(subject))
        uniform_input, new_time = interpulation.getUniformSampled(input, xrange(len(input)), numOfFeatures)
        sub_uniform.plot( xrange(numOfFeatures), uniform_input)
        data.append(uniform_input)
        tags.append(subject)
        plt.xlabel('Time (in frames)')
        plt.ylabel(joint + ' angle')
        plt.title('subject: ' + str(subject))
hits=0.0
counter = 0.0
testFactors = np.linspace(0.03, 0.97, 20)
scores = []
clfs = []
testSize = 35
testAmount = 100
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
    from sklearn.neighbors import KNeighborsClassifier
    knn = KNeighborsClassifier()
    knn.n_neighbors = 5
    knn.weights = 'distance' 
    fit = knn.fit(trainData, trainTags)
    res = knn.predict(dataTest)
    gc.collect()
    for i in xrange(testSize):
        if(res[i] == tagsTest[i]):
            hits+=1
        counter+=1
        i+=1
score = hits/counter*100
print score

outFile = 'out.txt'
out = open(outFile, 'r')
scores = []
testSizes = []
for line in out:
    splited = line.split()
    scores.append(splited[0])
    testSizes.append(splited[1])
plt.figure()
plt.plot(testSizes, scores)
plt.xlabel('Test set size)')
plt.ylabel('Prediction precision')
plt.title('Prediction precision for 4 subjects, data set size is 43')
plt.show()








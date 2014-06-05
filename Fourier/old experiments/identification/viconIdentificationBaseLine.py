from utils.vicon.amcParser import getAMCperiod
from utils.periodAnalysisUtils import alignByMax
import matplotlib.pyplot as plt
import math
import numpy as np
import utils.interpulation as inter
from sklearn import datasets
from sklearn.neighbors import KNeighborsClassifier
from utils.misc import crossValidate.crossValidate
import copy

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
        new_time, uniform_input = inter.getUniformSampled(xrange(len(input)), input, numOfFeatures)
        sub_uniform.plot( xrange(numOfFeatures), uniform_input)
        data.append(uniform_input)
        tags.append(subject)
        plt.xlabel('Time (in frames)')
        plt.ylabel(joint + ' angle')
        plt.title('subject: ' + str(subject))

cl = KNeighborsClassifier()
cl.n_neighbors = 5
cl.weights = 'distance' 
testSize = 35
score = crossValidate(cl, data, tags, testSize)


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







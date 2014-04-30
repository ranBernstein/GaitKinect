from utils.amcParser import getAMCperiod
from utils.periodAnalysisUtils import alignByMax
import matplotlib.pyplot as plt
import math
import numpy as np
import utils.interpulation as inter
from sklearn import datasets
from sklearn.neighbors import KNeighborsClassifier
from utils.crossValidate import crossValidate
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
out = open('out', 'w')
out.write('@relation weka.kuku\n\n')
for i in range(numOfFeatures):
    out.write('@attribute a'+str(i)+ ' numeric\n')
st=''
for i,s in enumerate(subjects):
    st+='sub'+str(s)
    if i!= len(subjects)-1:
        st+=','
out.write('@attribute class {'+st+'}\n\n@data\n\n')
for subject in subjects:
    for stride in xrange(1,13):
        file = '../AMCs/subjects/' + str(subject) + '/' + str(stride) + '.amc'
        try:
            input = getAMCperiod(joint, file)
        except:
            continue
        input = alignByMax(input)
        sub =  fig.add_subplot(frameSize*110 + subjects.index(subject))
        sub.plot(range(len(input)), input)
        sub_uniform = fig_uniform.add_subplot(frameSize*110 + subjects.index(subject))
        new_time, uniform_input = inter.getUniformSampled(xrange(len(input)), input, numOfFeatures)
        for angle in uniform_input:
            out.write(str(angle)+',')
        out.write(str(subject)+'\n')
        sub_uniform.plot( xrange(numOfFeatures), uniform_input)
        data.append(uniform_input)
        tags.append(subject)
        plt.xlabel('Time (in frames)')
        plt.ylabel(joint + ' angle')
        plt.title('subject: ' + str(subject))
"""
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
"""
plt.show()







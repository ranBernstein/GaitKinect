from utils.vicon.amcParser import getAMCperiod
from utils.utils import alignByMax
import matplotlib.pyplot as plt
import math
import numpy as np
import utils.interpulation as inter
from scipy import stats
from sklearn import datasets
from sklearn.neighbors import KNeighborsClassifier
import copy
lenVec = 100
joints = ['rradius', 'lradius', 'rtibia', 'ltibia', 'rwrist', 'lwrist', 'lfoot', 'rfoot', 'lowerback', 'upperback', 'head']
specialOperators = [np.mean, np.std, stats.skew, stats.kurtosis, len, np.max, np.min]
numOfFeatures = len(joints)*(len(specialOperators) +lenVec)
subjects = [2, 5, 6, 7, 8, 12, 16, 35 ,39]
frameSize = math.ceil(np.sqrt(len(subjects)))
fig = plt.figure()

fig_uniform = plt.figure()
data = []
tags = []
out = open('out.arff', 'w')
out.write('@relation weka.kuku\n\n')
for i in range(numOfFeatures):
    out.write('@attribute a'+str(i)+ ' numeric\n')
st=''
for i,s in enumerate(subjects):
    st+=str(s)
    if i!= len(subjects)-1:
        st+=','
out.write('@attribute class {'+st+'}\n\n@data\n\n')
for subject in subjects:
    for stride in xrange(1,13):
        file = '../AMCs/subjects/' + str(subject) + '/' + str(stride) + '.amc'
        features = []
        for joint in joints:
            try:
                input = getAMCperiod(joint, file)
            except:
                continue
            input = alignByMax(input)
            sub =  fig.add_subplot(frameSize*110 + subjects.index(subject))
            sub.plot(range(len(input)), input)
            sub_uniform = fig_uniform.add_subplot(frameSize*110 + subjects.index(subject))
            
            specialFeatures = [op(input) for op in specialOperators]
            new_time, uniform_input = inter.getUniformSampled(xrange(len(input)), input, lenVec)
            features += specialFeatures 
            features += uniform_input.tolist()
            sub_uniform.plot( xrange(len(uniform_input)), uniform_input)
            data.append(uniform_input)
            tags.append(subject)
            plt.xlabel('Time (in frames)')
            plt.ylabel(joint + ' angle')
            plt.title('subject: ' + str(subject))
        if len(features)==0:
            continue
        for f in features:
            out.write(str(f)+',')
        out.write(str(subject)+'\n')
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
#plt.show()







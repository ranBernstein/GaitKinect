import numpy as np
import numpy.random as rnd
import matplotlib.pyplot as plt 
import scipy.linalg as lin
import re
from scipy.signal import argrelextrema
from utils.amcParser import getAMCperiod
from cluster import HierarchicalClustering
from utils.stitching import MAXIMA_ORDER, CLUSTER_COEFF, plotParts


file = 'AMCs/598.amc'
joint = 'rtibia'
list = getAMCperiod(joint, file)
a = np.array(list)
localMax = argrelextrema(a, np.greater, 0, MAXIMA_ORDER)
plt.plot(list)
#plt.scatter(localMax, a.take(localMax))
amplitude = np.max(a) - np.min(a)
cl = HierarchicalClustering(a.take(localMax)[0].tolist(), lambda x,y: abs(x-y))
clusters = cl.getlevel(int(amplitude*CLUSTER_COEFF))
colors = ['blue', 'green', 'red', 'yellow', 'gray']
clustersIndices = []
longest = None
maxLength = 0
for c, cluster in zip(colors, clusters):
    if(len(cluster) > maxLength):
        longest = cluster 
        maxLength = len(cluster)  
    clusterIndices = []
    for y in cluster:
        x = list.index(y)
        clusterIndices.append(x)
        plt.scatter(x, y, color=c)
    clustersIndices.append(clusterIndices)
clusters.remove(longest)
maxLength = 0
secondLongets = None
for cluster in clusters:
    if(len(cluster) > maxLength):
        secondLongets = cluster
        maxLength = len(cluster) 
longestIndices = []
for y in longest:
    longestIndices.append(list.index(y))
secondLongestIndices = []
for y in secondLongets:
    secondLongestIndices.append(list.index(y))
plt.figure()
plt.scatter(longestIndices, longest, color='red')
plt.scatter(secondLongestIndices, secondLongets, color='blue')
plt.plot(list)

stances = []
swings = []
mergedIndices = secondLongestIndices + longestIndices
mergedIndices.sort()
for i, index in enumerate(mergedIndices[:-1]):
    segment = mergedIndices[i+1] - mergedIndices[i]
    if(list[mergedIndices[i]] < list[mergedIndices[i+1]]):
        stances.append(segment)
    else:
        swings.append(segment)
        
print stances
print swings
plt.show()

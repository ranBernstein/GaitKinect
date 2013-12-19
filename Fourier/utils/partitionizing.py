import numpy as np
import numpy.random as rnd
import matplotlib.pyplot as plt 
import scipy.linalg as lin
import re
from scipy.signal import argrelextrema
from amcParser import getAMCperiod
from cluster import HierarchicalClustering
from stitching import MAXIMA_ORDER, CLUSTER_COEFF, plotParts
"""
file = 'AMCs/673.amc'
joint = 'ltibia'
list = getAMCperiod(joint, file)
"""
def breakToPeriods(arg, file=False):
    list = []
    if(file):
        file = open(arg, 'r')
        for line in file:
            list.append(float(line))
    else:
        list = arg
    a = np.array(list)
    #plt.plot(list)
    tmp = argrelextrema(a, np.greater, 0, MAXIMA_ORDER)
    #plt.scatter(tmp, a.take(tmp))
    #print tmp
    #print a.take(tmp)[0]
    amplitude = np.max(a) - np.min(a)
    cl = HierarchicalClustering(a.take(tmp)[0].tolist(), lambda x,y: abs(x-y))
    clusters = cl.getlevel(int(amplitude*CLUSTER_COEFF))
    if(len(clusters) == 0):
        return []
    #print clusters
    max = 0
    longestSeq = None
    if(len(clusters) == len(tmp)):
        longestSeq = clusters
    else:
        for cluster in clusters:
            l = len(cluster)
            if(l>max):
                longestSeq = cluster
                max = l
    #print longestSeq
    if(len(longestSeq) < 2):
        return []
    averageLength = len(list)/len(longestSeq)  
    periods = []
    indices = [list.index(x) for x in longestSeq]
    indices.sort()
    open = indices[0]
    for i in indices[1:]:
        #plt.figure()
        close = i
        strideLen = close - open
        if(strideLen > 0.7*averageLength and strideLen < 1.8*averageLength):
            period = list[open:close]
            periods.append(period)
        else:
            #print strideLen, averageLength
            pass
        open = close
        #plt.plot(period)
    #periods = periods[1:]
    plotParts(periods)
    #plt.show()
    return periods
"""
#f = open('../outputs/stitching/greedy_with_noise/stitched.txt', 'r')
breakToPeriods('../outputs/stitching/greedy_with_noise/stitched.txt', True)
"""
import numpy as np
import numpy.random as rnd
import matplotlib.pyplot as plt 
import scipy.linalg as lin
import re
from scipy.signal import argrelextrema
from amcParser import getAMCperiod
from cluster import HierarchicalClustering

"""
file = 'AMCs/673.amc'
joint = 'ltibia'
list = getAMCperiod(joint, file)
"""
#f = open('outputs/stitching/greedy_with_noise/stitched.txt', 'r')
def breakToPeriods(arg):
    list = []
    if(type(arg) is str):
        file = open(arg, 'r')
        for line in file:
            list.append(float(line))
    else:
        list = arg
    a = np.array(list)
    plt.plot(a)
    tmp = argrelextrema(a, np.greater, 0, 10)
    plt.scatter(tmp, a.take(tmp))
    print tmp
    print a.take(tmp)[0]
    amplitude = np.max(a) - np.min(a)
    cl = HierarchicalClustering(a.take(tmp)[0].tolist(), lambda x,y: abs(x-y))
    clusters = cl.getlevel(amplitude/10)
    print clusters
    max = 0
    longestSeq = None
    for cluster in clusters:
        l = len(cluster)
        if(l>max):
            longestSeq = cluster
            max = l
    print longestSeq    
    open = 0
    periods = []
    indices = [list.index(x) for x in longestSeq]
    indices.sort()
    for i in indices:
        #plt.figure()
        close = i
        period = list[open:close]
        periods.append(period)
        open = close
        #plt.plot(period)
    periods = periods[1:]
    #plt.show()
    return periods
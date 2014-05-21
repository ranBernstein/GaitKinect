import numpy as np
from scipy.signal import argrelextrema
from cluster import  HierarchicalClustering
import scipy.stats as stats
import matplotlib.pyplot as plt
import utils.stitching as st
"""
file = 'AMCs/673.amc'
joint = 'ltibia'
list = getAMCperiod(joint, file)
"""
def breakToPeriods(arg, maximaOrder=20, clusteringGranularity = 0.5, file=False):
    inputAsList = []
    if(file):
        file = open(arg, 'r')
        for line in file:
            inputAsList.append(float(line))
    else:
        inputAsList = arg
    inputAsList = inputAsList if type(inputAsList) is list else inputAsList.tolist()
    a = np.array(inputAsList)
    localMax = argrelextrema(a, np.greater, 0, maximaOrder)[0].tolist()
    try:
        amplitude = np.max(a) - np.min(a)
    except:
        return []
    cl = HierarchicalClustering(a.take(localMax).tolist(), lambda x,y: abs(x-y))
    clusters = cl.getlevel(int(amplitude*clusteringGranularity))
    if(len(clusters) == 0):
        return []
    #print clusters
    max = 0
    longestSeq = None
    if(len(clusters) == len(localMax)):#It clustered every maxima differently
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
    averageLength = len(inputAsList)/len(longestSeq)  
    periods = []
    indices = [inputAsList.index(x) for x in longestSeq]
    indices.sort()
    open = indices[0]
    for i in indices[1:]:
        #plt.figure()
        close = i
        strideLen = close - open
        if(strideLen > 0.5*averageLength and strideLen < 1.8*averageLength):
            period = inputAsList[open:close]
            periods.append(period)
        else:
            pass
        open = close
    return periods

def plotStas(periods, title):
    st.plotParts(periods)
    vec = [len(period) for period in periods]
    plt.figure()
    mean = np.mean(vec)
    std = np.std(vec)
    skew =stats.skew(vec)
    ku = stats.kurtosis(vec)
    plt.title(title +' mean: '+ str(mean)+' std: '+str(std)+' skew: '+str(skew)+' kurtosis: '+str(ku))
    plt.scatter(range(len(vec)), vec)
    plt.figure()
    plt.hist(vec)
"""
#f = open('../outputs/stitching/greedy_with_noise/stitched.txt', 'r')
breakToPeriods('../outputs/stitching/greedy_with_noise/stitched.txt', True)
"""
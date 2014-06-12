import numpy as np
import matplotlib.pyplot as plt
import itertools
import random
import copy
import utils.interpulation as interpulation
from operator import add, sub
import math
from scipy.interpolate import interp1d
import utils.LPF as LPF
from utils.vicon.amcParser import getAMCInput
#import utils.lcss as lcs 
EPSILON_FACTOR = 0.15 
GAP_FACTOR = 0.15
MEAN_COEFF = 0.13
STD_COEFF = 0.09
MAXIMA_ORDER = 7
CLUSTER_COEFF = 0.15
OVERLAP_FACTOR = 0.1

def isEqual(a, b, gap=0,  epsilon_factor=EPSILON_FACTOR, gap_factor=GAP_FACTOR):
    #return a==b
    epsilon = np.abs(float(a+b)*epsilon_factor)
    if(gap == 0):
        return np.abs(a-b) <=  epsilon
    if(np.abs(gap) > np.abs(float(a+b)*gap_factor)):
        return np.abs(a - b) <=  epsilon
    return np.abs(a - gap - b) <=  epsilon

def compareHashed(t1, t2):
    try:
        some_object_iterator = iter(t1)
    except TypeError, te:
        return isEqual(t1, t2)
    #t1 and t2 are iterables
    for e1, e2 in zip(t1, t2):
        if(not isEqual(e1, e2)):
            return False
    return True

def myHash(seq):
    return seq
    return hash(tuple(seq))
    #return seq[0], seq[-1], np.mean(seq), np.std(seq)

def shift(l, n):
    return l[n:] + l[:n]     
    
    
def getAMCperiod(joint, file):
    f=None
    try:
        f = open(file, 'r')
    except IOError:
        return []
    input = []
    for line in f:
        if joint in line:
            input.append(float(line.split()[1]))
    return input


def cost(vec):
    #Fourier
    """
    trans = np.fft.fft(vec)
    absTrans = np.absolute(trans)
    absTrans.sort()
    coeffAmount = 13
    mainSum=0
    for i in xrange(1, min(coeffAmount+1, len(absTrans))):
        mainSum += absTrans[-i]
    return mainSum/np.sum(absTrans)
    """
    sum=0.0
    for i in xrange(len(vec)-1):
        sum+= (vec[i+1] - vec[i])**2
    return sum / float(len(vec)) 


def createParts(input, plotNoise=False,  partsAmount = 9, noiseVariance = 6, cleanFunc=LPF.clean):                
    original_parts = []
    noisy_parts = []
    parts = []
    partsIndices = xrange(partsAmount)
    chunckSize = len(input)/partsAmount
    if(chunckSize < 2):
        raise 'input too short'
    prefixes = {}
    sufixes = {}
    overlapFactor = 1
    for i in partsIndices:
        start = max(0, i*chunckSize-random.randint(1, int(overlapFactor*chunckSize)))
        end = min((i+2)*chunckSize+random.randint(1, int(overlapFactor*chunckSize)), len(input))
        part = input[start:end]
        original_parts.append(part)
        #Adding noise
        noise = np.random.normal(0,noiseVariance,len(part))
        part = map(add, noise, part)
        noisy_parts.append(part)
        #part = cleanFunc(part)
        #parts.append(part)
    if(plotNoise):
        plotParts(noisy_parts)
    return noisy_parts

def plotParts(parts, xlabel = ' ', ylabel = ' ', titles = [' ']*100, xlim=None, ylim=None):
    fig = plt.figure()
    for i, part in enumerate(parts):
        frameSize = math.ceil(np.sqrt(len(parts)))
        try:
            curr = fig.add_subplot(frameSize,frameSize,i+1)
        except Exception, e:
            pass
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        plt.title(titles[i])
        if xlim is not None:
            plt.xlim(xlim)
        if ylim is not None:
            plt.ylim(ylim)
        curr.plot(part)

def appendFrac(whole, originalNext, averagedWhole=None):
    if(averagedWhole is None):
        averagedWhole =  copy.copy(whole)
    scaledNexts = interpulation.getScaledVectors(originalNext)
    longestOverlap = 0
    bestExtention = None
    bestOverlap = None
    for next in scaledNexts: 
        for j in reversed(xrange(1,len(next))):
            if(j > len(whole)-1):
                continue
            match = True
            gap = np.mean(whole[-j:]) - np.mean(next[:j])
            for i in xrange(j):
                if(not isEqual(whole[-j+i], next[i], gap)):
                    match = False
                    break
            if(match and j>longestOverlap):
                longestOverlap = j
                bestExtention = next[j:]
                bestOverlap = next[:j]
    if(bestExtention is not None):
        for i in xrange(len(bestOverlap)):
            averagedWhole[-i] = ( whole[-i] + bestOverlap[-i])/2.0
            pass
        return whole + bestExtention.tolist(), averagedWhole + bestExtention.tolist()
    return whole, averagedWhole

def checkMoments(vec1, vec2,  m1=MEAN_COEFF, m2=STD_COEFF, epsilon=EPSILON_FACTOR, gap=GAP_FACTOR, overlap=OVERLAP_FACTOR):
    amplitude = np.max(vec1 + vec2) - np.min(vec1 + vec2)
    mean_diff = np.abs(np.mean(vec1) - np.mean(vec2))
    diffVec = map(sub, vec1, vec2)
    diff_std = np.std(diffVec)
    if(mean_diff < m1*amplitude and diff_std<m2*amplitude):
        return True
    else:
        for i in xrange(len(vec1)):
            if(not isEqual(vec1[i], vec2[i], mean_diff, epsilon, gap)):
                return False
    return True

def appendFracaveraged(whole, originalNext, m1=MEAN_COEFF, m2=STD_COEFF, epsilon=EPSILON_FACTOR, gap=GAP_FACTOR, overlap=OVERLAP_FACTOR):
    scaledNexts = interpulation.getScaledVectors(originalNext)
    longestOverlap = 0
    bestExtention = None
    bestOverlap = None
    for next in scaledNexts: 
        for j in reversed(xrange(int(len(next)*OVERLAP_FACTOR),len(next))):
            if(j > len(whole)-1):
                continue
            match = checkMoments(whole[-j:],next[:j],  m1, m2, epsilon, gap, overlap)
            if(match and j>longestOverlap):
                longestOverlap = j
                bestExtention = next[j:]
                bestOverlap = next[:j]
    if(bestExtention is not None):
        for i in xrange(len(bestOverlap)):
            whole[-i] = ( whole[-i] + bestOverlap[-i])/2.0
            pass
        return whole + bestExtention.tolist()
    return whole

def prependFrac(whole, originalNext,  m1=MEAN_COEFF, m2=STD_COEFF, epsilon=EPSILON_FACTOR, gap=GAP_FACTOR, overlap=OVERLAP_FACTOR):
    scaledNexts = interpulation.getScaledVectors(originalNext)
    longestOverlap = 0
    bestExtention = None
    bestOverlap = None
    for next in scaledNexts:
        for j in reversed(xrange(int(OVERLAP_FACTOR*len(next)),len(next))):
            if(j > len(whole)-1):
                continue
            match = checkMoments(whole[:j],next[:j],  m1, m2, epsilon, gap, overlap)
            if(match and j>longestOverlap):
                longestOverlap = j
                bestExtention = next[:-j]
                bestOverlap = next[-j:]
    if(bestExtention is not None):
        for i in xrange(len(bestOverlap)):
            #whole[i] = ( whole[i] + bestOverlap[i])/2.0
            pass
        return whole + bestExtention.tolist() 
    return whole

def stitchByOrder(parts):
    byOrder = copy.copy(parts[0])
    averaged = copy.copy(byOrder)
    for part in parts[1:]:
        byOrder, averaged = appendFrac(byOrder, part, averaged)
    
    cleaned, cleaned_time = LPF.clean(averaged) 
    plt.figure()
    plt.title('Stitching by order')
    plt.plot(xrange(len(input)), input, color='blue', label='original, SM='+str(cost(input)))
    plt.plot(xrange(len(byOrder)), byOrder, color='black', label='byOrder, SM='+str(cost(byOrder)))
    plt.plot(xrange(len(averaged)), averaged, color='red', label='byOrder and averaged, SM='+str(cost(averaged)))
    plt.plot(xrange(len(cleaned)), cleaned, color='green', label='byOrder and LPF and averaged, SM='+str(cost(cleaned)))
    plt.legend().draggable()

def stitch(parts, m1=MEAN_COEFF, m2=STD_COEFF, epsilon=EPSILON_FACTOR, gap=GAP_FACTOR, overlap=OVERLAP_FACTOR):
    """
    MEAN_COEFF=m1
    STD_COEFF=m2
    EPSILON_FACTOR=epsilon
    OVERLAP_FACTOR=overlap
    GAP_FACTOR=gap
    """
    #greedy
    parts.sort()
    parts.reverse()
    averaged = copy.copy(parts[0])
    notUsed = []
    for part in parts[1:]:
        lenBefore = len(averaged)
        #greedy, kuku = appendFrac(greedy, part, averaged)
        averaged = appendFracaveraged(averaged, part,  m1, m2, epsilon, gap, overlap)
        if(lenBefore == len(averaged)):
            notUsed.append(part)   
    counter = 0
    for part in notUsed:
        lenBefore = len(averaged)
        averaged = prependFrac(averaged, part,  m1, m2, epsilon, gap, overlap)
        if(len(averaged) != lenBefore):
            counter+=1
            notUsed.remove(part)
    """
    for part in notUsed:
        a = np.sum(averaged)
        lcs.lcs(averaged, part, isEqual)
        #if(a!=np.sum(averaged)):
         #   print 'kuku'
    """
    clean, clean_time = LPF.clean(averaged)
    plt.figure()
    plt.plot(clean)
    return clean

"""
subject = 8
joint = 'rtibia'
index =0
partsAmount =9
input = getAMCInput(joint, subject, index)
parts = createParts(input, partsAmount)
plotParts(parts)
stitched = stitch(parts)
plt.figure()
plt.title('Greedy with second moment')
#plt.plot(xrange(len(greedy)), greedy, color='black', label='greedy')
plt.plot(xrange(len(stitched)), stitched, color='red', label='greedy and averaged')
clean, clean_time = LPF.clean(stitched)
#f = open('outputs/stitching/greedy_with_noise/stitched.txt', 'w')
#f.flush()
#f.writelines([str(x)+'\n' for x in clean])
#f.close()
plt.plot(xrange(len(clean)), clean, color='green', label='greedy and averaged and clean')
plt.legend().draggable()
plt.show()
""" 
    
    
    
    
    
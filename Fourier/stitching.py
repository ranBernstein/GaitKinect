import numpy as np
import matplotlib.pyplot as plt
import itertools
import random
import copy
import interpulation
from operator import add, sub
import math
from scipy.interpolate import interp1d
import LPF

EPSILON_FACTOR = 0.2 
MEAN_COEFF = 0.1
STD_COEFF = 0.1
noiseVariance = 6

def isEqual(a, b, gap=0):
    #return a==b
    epsilon = np.abs(float(a+b)*EPSILON_FACTOR)
    if(gap == 0):
        return np.abs(a-b) <=  epsilon
    if(np.abs(gap) > np.abs(float(a+b)/10.0)):
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
                
t = np.linspace(0.0, 2*np.pi, num=100)
subject = 2
sample = 1
file = 'AMCs/subjects/' + str(subject) + '/origin1-2.amc'  
#file = 'AMCs/subjects/' + str(subject) + '/' + str(sample) + '.amc'
joint = 'ltibia'
input = getAMCperiod(joint, file)
partsAmount = 9

original_parts = []
noisy_parts = []
parts = []
partsIndices = xrange(partsAmount)
chunckSize = len(input)/partsAmount
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
    part, clean_time = LPF.clean(part)
    parts.append(part)

def plotParts(parts):
    fig = plt.figure()
    for part in parts:
        frameSize = math.ceil(np.sqrt(partsAmount))
        curr = fig.add_subplot(frameSize*110 + parts.index(part)+1)
        curr.plot(xrange(len(part)), part)
plotParts(original_parts)
plotParts(noisy_parts)
plotParts(parts)

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

def checkMoments(vec1, vec2):
    amplitude = np.max(vec1 + vec2) - np.min(vec1 + vec2)
    mean_diff = np.abs(np.mean(vec1) - np.mean(vec2))
    diffVec = map(sub, vec1, vec2)
    diff_std = np.std(diffVec)
    if(mean_diff < MEAN_COEFF*amplitude and diff_std<STD_COEFF*amplitude):
        return True
    else:
        for i in xrange(len(vec1)):
            if(not isEqual(vec1[i], vec2[i], mean_diff)):
                return False
    return True

def appendFracaveraged(whole, originalNext):
    scaledNexts = interpulation.getScaledVectors(originalNext)
    longestOverlap = 0
    bestExtention = None
    bestOverlap = None
    for next in scaledNexts: 
        for j in reversed(xrange(1,len(next))):
            if(j > len(whole)-1):
                continue
            match = checkMoments(whole[-j:],next[:j])
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

def prependFrac(whole, originalNext):
    scaledNexts = interpulation.getScaledVectors(originalNext)
    longestOverlap = 0
    bestExtention = None
    bestOverlap = None
    for next in scaledNexts:
        for j in reversed(xrange(1,len(next))):
            if(j > len(whole)-1):
                continue
            match = checkMoments(whole[:j],next[:j])
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


#greedy
parts.sort()
parts.reverse()
greedy = copy.copy(parts[0])
averaged = copy.copy(greedy)
notUsed = []
for part in parts[1:]:
    lenBefore = len(greedy)
    #greedy, kuku = appendFrac(greedy, part, averaged)
    averaged = appendFracaveraged(averaged, part)
    if(lenBefore == len(averaged)):
        notUsed.append(part)   
counter = 0
for part in notUsed:
    lenBefore = len(averaged)
    averaged = prependFrac(averaged, part)
    if(len(averaged) != lenBefore):
        counter+=1
print len(notUsed) -  counter



plt.figure()
plt.title('Greedy with second moment')
#plt.plot(xrange(len(greedy)), greedy, color='black', label='greedy')
plt.plot(xrange(len(averaged)), averaged, color='red', label='greedy and averaged')
clean, clean_time = LPF.clean(averaged)
f = open('outputs/stitching/greedy_with_noise/stitched.txt', 'w')
f.flush()
#f.writelines([str(x)+'\n' for x in clean])
f.close()
plt.plot(xrange(len(clean)), clean, color='green', label='greedy and averaged and clean')
plt.legend().draggable()
plt.show()
  
    
    
    
    
    
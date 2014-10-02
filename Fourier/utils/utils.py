import numpy as np
import LPF
from stitching.algorithm import stitchingLoop as sl
from scipy.interpolate import interp1d

def toList(vec):
    if type(vec) is tuple:
        vec = list(vec)
    else:
        vec = vec if type(vec) is list else vec.tolist()
    return vec 

def alignByMaxMany(inputs):
    ret = []
    for input in inputs:
        ret.append(alignByMax(input))
    return ret
    

#align all cycles to the same phase
def alignByMax(input):
    maxIndex = -1
    maxValue = None
    i = 0
    for e in input:
        if (maxValue==None) or (e > maxValue):
            maxIndex = i
            maxValue = e
        i+=1
    l = len(input)
    alignedInput = []
    for i in range(l):
        newIndex = int((maxIndex + i)%l)
        alignedInput.append(input[newIndex])
    return alignedInput

def alignBySmall(vec1, vec2, compareFunc=sl.euclidean):
    big, small = (vec1, vec2) if len(vec1) > len(vec2) else (vec2, vec1)
    bestGrade = 0
    bestVec = None
    for shift in xrange(len(big)):
        newBig = big[-shift:] + big[:-shift]
        grade = compareFunc(small, newBig[:len(small)])
        if(grade > bestGrade):
            bestGrade = grade
            bestVec = newBig
    return (bestVec, vec2) if len(vec1) > len(vec2) else (vec1, bestVec)

def alignByBig(vec1, vec2, compareFunc=sl.euclidean):
    try:
        big, small = (vec1, vec2) if len(vec1) > len(vec2) else (vec2, vec1)
    except Exception, e:
        pass
    bestGrade = 0
    bestOffset = None
    for offset in xrange(len(big) - len(small)):
        overLap = big[offset:(offset+len(small))]
        grade = compareFunc(small, overLap)
        if(grade > bestGrade):
            bestGrade = grade
            bestOffset = offset
    return (bestOffset, 0) if len(vec1) < len(vec2) else (0, bestOffset)
        
def deriveTimeSeries(time, values):
    derived = []
    derivedTime = []
    for i in xrange(len(time)-1):
        deltaT= float(time[i+1] - time[i])
        deltaY= float(values[i+1] - values[i])
        derived.append(deltaY/deltaT)
        derivedTime.append((time[i+1] + time[i])/2)
    return derivedTime, derived

def binaryByMean(input):
    tmpInput = []
    mean = np.mean(np.array(input))
    for e in input:
        if(e > mean):
            tmpInput.append(1)
        else:
            tmpInput.append(-1)
    return tmpInput

def binaryByMedian(input):
    tmpInput = []
    median = np.median(np.array(input))
    for e in input:
        if(e > median):
            tmpInput.append(1)
        else:
            tmpInput.append(-1)
    return tmpInput

def smoothOutliers(input):
    tmpInput = []
    tmpInput.append(input[0])
    for i in xrange(1, len(input)-1):
        if(input[i] != input[i-1] and input[i]!=input[i+1]):
            tmpInput.append(-1*input[i])
        else:
            tmpInput.append(input[i])
    tmpInput.append(input[-1])
    return tmpInput

def dropOutliers(input, time=None):
    tmpInput = []
    tmpTime = []
    std = np.std(input)
    if(time is None):
        time = xrange(len(input))
    clean, clean_time = LPF.clean(input, time)
    f = interp1d(clean_time, clean, kind='cubic')
    tmpTime.append(time[0])
    tmpInput.append(input[0])
    for i in xrange(1, len(input)):
        if(np.abs(input[i] - f(time[i])) > 1*std):
            pass
        else:
            tmpInput.append(input[i])
            tmpTime.append(time[i])
    return tmpInput, tmpTime

def normalizeVector(vec):
    amplitude = float(max(np.abs(max(vec)), np.abs(min(vec))))
    return [v/amplitude-np.mean(vec) for v in vec]

def corr(v1,v2):
    return np.dot(v1,v2)/np.sqrt(np.dot(v1,v1)*np.dot(v2,v2))
    



    
    
    
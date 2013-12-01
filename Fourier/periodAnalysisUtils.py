import numpy as np

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
    
    
    
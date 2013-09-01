import matplotlib.pyplot as plt
import numpy as np
from Fourier import getFourier
from Cleaner import *
from matplotlib.mlab import PCA
from array import array
import matplotlib.cm as cm

samples = range(1,20)
#samplesNum = len(samples)
subjects = [8, 16, 35, 39]
#joint = 'rtibia'
numOfCoeffs = 9

def getAMCperiod(joint, file, period=False, start=0, end=0):
    f=None
    try:
        f = open(file, 'r')
    except IOError:
        return []
    input = []
    for line in f:
        if joint in line:
            input.append(float(line.split()[1]))
    if(period):
        input = input[start:end]  # getPeriod
    return input

def getLengthVector(subject):
    outputs = np.empty((0, 1), dtype=np.float)
    for sample in samples:
        fileName = 'AMCs/subjects/' + str(subject) + '/' + str(sample) + '.amc'
        sample= sample-1
        input = getAMCperiod('ltibia', fileName)
        if(len(input) == 0):
            return outputs
        outputs = np.concatenate((outputs, np.array([[len(input)]])), axis=0)
    return outputs   

def getFFT4subject(subject, joint, c):
    outputs = np.empty((0, 2*numOfCoeffs), dtype=np.float)
    for sample in samples:
        fileName = 'AMCs/subjects/' + str(subject) + '/' + str(sample) + '.amc'
        sample= sample-1
        input = getAMCperiod(joint, fileName)
        if(len(input) == 0):
            return outputs
        #align all cycles to the same phase
        maxIndex = -1
        maxValue = 0
        i = 0
        for e in input:
            if e > maxValue:
                maxIndex = i
                maxValue = e
            i+=1
        l = len(input)
        alignedInput = []
        for i in range(l):
            newIndex = int((maxIndex + i)%l)
            alignedInput.append(input[newIndex])
        input = alignedInput
        fft = np.fft.fft(input, numOfCoeffs)
        tmp = np.empty((1, 2*numOfCoeffs), dtype=np.float)
        for i in range(numOfCoeffs):
            tmp[0, 2*i] = fft[i].real
            tmp[0, 2*i+1] = fft[i].imag
        tmp[0, 0] = 0
        outputs = np.concatenate((outputs, tmp), axis=0)
    return outputs
    
colors = cm.rainbow(np.linspace(0, 1, len(subjects)))

def getMergedData(joints):
    input = None#np.empty((0, numOfCoeffs*2*len(joints)))
    tags =  np.empty(0)
    first = True
    for subject, c in zip(subjects, colors):
        samplesNum =  getLengthVector(subject).shape[0]
        currSamples = np.empty((samplesNum, 0))
        for joint in joints:
            if(joint == 'cycle_duration'):
                curr = getLengthVector(subject)
            else:
                curr = getFFT4subject(subject, joint, c)
            currSamples = np.concatenate((currSamples, curr), axis=1)
        currTags = np.empty(samplesNum)
        currTags.fill(subject)
        tags = np.concatenate((tags, currTags), axis=0)
        if(first):
            input = np.empty((0, currSamples.shape[1]))
            first = False
        input = np.concatenate((input, currSamples), axis=0)
    return input, tags
    
"""
joint = 'rtibia'
fileName = '39/origin4.amc'
file = 'AMCs/subjects/' + fileName
input = getAMCperiod(joint, file)
fig = plt.figure()
plt.xlim(0, len(input))
#ax = fig.add_subplot(111)
i= np.random.random(10)
plt.plot(range(len(input)), input)
plt.xlabel('Time (in frames)')
plt.ylabel(joint + ' angle')
fig.suptitle(fileName + ' - ' + joint, fontsize=14, fontweight='bold')
plt.show()
"""








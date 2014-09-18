import numpy as np
import math
import matplotlib.pyplot as plt 
from utils.vicon.amcParser import getAMCperiod
from utils.stitching.stitching import MAXIMA_ORDER, CLUSTER_COEFF, plotParts, createParts
import utils.stitching.stitching as loop
import utils.utils as ut
import utils.MovingAverage as ma

file = 'AMCs/598.amc'
joint = 'rtibia'
list = getAMCperiod(joint, file)
stride = list[112:251] 
list = ut.alignByMax(stride)
#list = ut.alignByMax(list)
noiseStdFactor = 0.04
amplitude = np.max(list) - np.min(list)
var = (amplitude*noiseStdFactor)**2
print var
partsAmount = 16
noisy_parts = createParts(list, True, partsAmount, var)
parts = ma.partsmovingAverage(noisy_parts)

frameSize = math.ceil(np.sqrt(len(parts)))
fig = plt.figure()
for i,part in enumerate(parts):
    curr = fig.add_subplot(frameSize,  frameSize, i+1)
    curr.plot(part)
        
merged, mergedDes = loop.stitch(parts)
print(len(merged))
bestFeatures = merged[-1]
des = mergedDes[-1]
outOff, listOff = ut.alignByBig(bestFeatures, list)
plt.figure()
plt.plot(xrange(listOff, listOff+len(list)), list, color='b')
plt.plot(xrange(outOff, outOff+len(bestFeatures)), bestFeatures, color='r')
sortingIndices = sorted(range(len(des)), key=lambda k: des[k][1])
frameSize = math.ceil(np.sqrt(len(sortingIndices)))

fig = plt.figure()
for step in xrange(1, len(sortingIndices)+1):
    curr = fig.add_subplot(frameSize, frameSize, step)
    for addedIndex in xrange(step):
        partNum = sortingIndices[addedIndex]
        part = parts[partNum]
        offset = des[partNum][0]
        curr.plot(xrange(offset, offset+len(part)),part)
        
fig = plt.figure()        
for step in xrange(1, len(sortingIndices)+1):
    curr = fig.add_subplot(frameSize, frameSize, step)
    for addedIndex in xrange(step):
        partNum = sortingIndices[addedIndex]
        part = noisy_parts[partNum]
        offset = des[partNum][0]
        curr.plot(xrange(offset, offset+len(part)),part)
"""
for partNum, offset in des.items():
    part = noisy_parts[partNum]
    plt.plot(xrange(offset, offset+len(part)),part)
"""
plt.show()


"""
stride = list[112:251] 
stride = ut.alignByMax(stride)
noiseVar = 12
frac1 = stride[:100]
frac1 = map(add, np.random.normal(0,noiseVar,len(frac1)), frac1)
plt.figure()
plt.plot(frac1)
frac1 = LPF.clean(frac1)
frac2 = stride[70:]
frac2 = map(add, np.random.normal(0,noiseVar,len(frac2)), frac2)
plt.figure()
plt.plot(frac2)
frac2 = LPF.clean(frac2)
"""
import utils.angleExtraction as ae
import matplotlib.pyplot as plt
import utils.MovingAverage as ma
import numpy as np
from scipy.ndimage.filters import maximum_filter
import utils.spikeDetection as spike
#fileName = 'inputs/Rachelle/spreadindAndClosing.skl'
fileName = 'inputs/Rachelle/expending and condencing.skl'
f = open(fileName, 'r')
headers = f.readline().split()
numOfJoints = (len(headers)-2)/4
jointsIndices = [2+4*index for index in range(numOfJoints)]
input = []
input2 = []
for line in f:
    lineInFloats=[float(v) for v in line.split()]
    #input.append(ae.calcDisFromIndices(lineInFloats, headers.index('HipCenter_X'), \
        #headers.index('WristRight_X')))
    input.append(ae.calcAverageJointDistanceFromCenter(lineInFloats, jointsIndices))
    #input.append(ae.calcAverageDistanceOfIndicesFromLine(lineInFloats, \
                #jointsIndices, headers.index('HipCenter_X'), headers.index('ShoulderCenter_X')))
plt.plot(input)
filtered = ma.movingAverage(input, 100, 1.03)
plt.plot(filtered)
m=np.mean(filtered)
change = [filtered[i+1]-filtered[i] for i in range(len(filtered)-1)]
changeForPlot = [100*x+m for x in change]
plt.plot(changeForPlot)
#plt.figure()
plt.plot(spike.clusterByPercemtile(change, 700, 90))
#plt.figure()
plt.show()    
import utils.kinect.angleExtraction as ae
import utils.stitching.stitching.quantization as qu
import matplotlib.pyplot as plt
import utils.oldKinectExtractor as ke
import utils.stitching.stitching as st
import utils.stitching.stitching.mineByPattern as mbp
from numpy import linalg as LA
import copy

fileName = 'inputs/ran_5_2_14_840.skl'
joint = 'AnkleRight_X'
time, values = ae.getAngleVec(fileName, joint, True)
disFactor=0.2
numOfClusters = 6
minimalCluster = 10
fracs = ke.clusterByTime(time, values, False, minimalCluster)
#originalFracs = copy.deepcopy(fracs)
prob = 0.05
fracs = ke.filterOutliers(fracs, False, prob)
i=0
parts, kuku = ke.cleanFracs(fracs, False)
pattern = [14, 15, 17, 19, 24, 28, 33, 33, 33, 33, \
           33, 33, 28, 24, 19, 17, 15, 14,\
           12, 12, 14, 15, 16, 17.5, 17.5, 17.5, \
           16, 15, 14, 13, 12, 12]


i=1
framSize = 4
groupSize = framSize**2
minedParts = []
for part in parts:
    index = i%groupSize
    retVal = qu.getAtomFromFrac(part, pattern, qu.extractPartialPattern)
    if retVal is None:
        continue
    frac,  dis, vecAtom, bias, bestScale, temporalScale, partOffset,\
        cycleOffset = retVal
    if(index==1):
        fig1 = plt.figure()
        fig2 = plt.figure()
    curr2 = fig2.add_subplot(framSize,framSize,index)
    curr = fig1.add_subplot(framSize,framSize,index)
    print str(i) +  ': dis: ' + str(dis) + ' offset: ' + str(cycleOffset)
    #plt.title('bias: ' + str(bias) + ' scale: ' + str(bestScale) + 
    #    ' bestTemporalScale: ' + str(temporalScale) + ' dis: ' + str(dis))
    plt.title(str(i))
    plt.ylim((0,50))
    curr.plot(part, c='b')
    rng = xrange(partOffset, partOffset + len(frac))
    curr.plot(rng, vecAtom, c='g')
    curr.plot(rng, frac, c='r') 
    
    rng = xrange(cycleOffset, cycleOffset + len(frac))
    plt.xlim((0, 50))
    plt.ylim((0,50))
    curr2.plot(rng, vecAtom)
    curr2.plot(rng, frac)

    minedParts.append((frac, cycleOffset, [i]))
    if(i>=3*groupSize):
        break
    i+=1
originalParts= copy.deepcopy(minedParts)
minedParts = mbp.matchFracsByPositionInCycle(minedParts)

fig = plt.figure()
i = 1
strides = []
for frac, offset, newList in minedParts:
    curr = fig.add_subplot(framSize,framSize,i)
    rng = xrange(offset, offset+len(frac))
    plt.xlim((0,50))
    plt.ylim((0,50))
    curr.plot(rng, frac, c='b')
    for l in newList:
        merged, off, kuku = originalParts[l-1]
        rng = xrange(off, off+len(merged))
        curr.plot(rng, merged, label=str(l))
    curr.legend().draggable(True)
    i+=1
    if len(frac) > 30:
        strides.append(frac)
#plt.plot(minedParts[0][0])
st.plotParts(strides)
plt.show()


















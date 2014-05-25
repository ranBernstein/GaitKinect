import matplotlib.pyplot as plt
import utils.angleExtraction as ae
import utils.oldKinectExtractor as ke
import utils.stitching as st
import numpy as np
import utils.quantization as qu
import utils.mineByPattern as mbp
import copy
import utils.MovingAverage as ma
import utils.partitionizing as prt

fileName = 'myKinect/i1.skl'
joint = 'KneeLeft_X'
time, angles= ae.getAngleVec(fileName, joint, True)

#Extracting clean fractions
minimalCluster=20
fracs = ke.clusterByTime(time, angles, False, minimalCluster)
prob = 0.1
fracs = ke.filterOutliers(fracs, False, prob)
i=0
cleanedParts, _ = ke.cleanFracs(fracs, False, 20, 1.1)
#st.plotParts(cleanedParts)

#Creating pattern to mine for
up = np.linspace(40, 70, 20)
start = 20
end = 45
up = (np.linspace(start,end,15)).tolist()
down = list(reversed(up))
pattern = [start, start, start] + up + ([end]*5) + down + [start, start, start]
lenOfCycle = len(pattern)
#plt.figure()
#plt.plot(pattern)
fig = plt.figure()
framSize= np.ceil(np.sqrt(len(cleanedParts)))
minedParts = []
minedPartsAsList = []
dises = []
threshold = 0
sizeFactor=2
#cleanedParts = cleanedParts[:3]
lengths = []
for index, part in enumerate(cleanedParts):
    retVal = qu.getAtomFromFrac(part, pattern, sizeFactor)
    if retVal is None:
        continue
    frac,  dis, vecAtom, bias, bestScale, temporalScale, partOffset,\
        cycleOffset = retVal
    if cycleOffset+len(frac)>np.ceil(temporalScale*lenOfCycle):
        print 'muku', index
    curr = fig.add_subplot(framSize,framSize,index+1)
    plt.title('dis: '+str(dis)+'\n temporalScale: ' + str(temporalScale)+ 
              ',\n scale: '+str(bestScale))
    #plt.ylim((0,50))
    curr.plot(part, c='b')
    rng = xrange(partOffset, partOffset + len(frac))
    curr.plot(rng, vecAtom, c='g')
    curr.plot(rng, frac, c='r') 
    threshold +=dis
    minedParts.append((frac, cycleOffset, [index]))
    minedPartsAsList.append(frac)
    dises.append(dis)
    lengths.append(len(frac))
#st.plotParts(minedPartsAsList)



#Filter the best matches
threshold = np.percentile(dises, 60)
newMinedParts=[]
newMinedPartsAsList=[]
for i, dis in enumerate(dises):
    if dis<threshold:
        newMinedPartsAsList.append(minedPartsAsList[i])
        newMinedParts.append(minedParts[i])
minedPartsAsList = newMinedPartsAsList
minedParts = newMinedParts
st.plotParts(minedPartsAsList, 'Frames', 'Angle', lengths)
#plt.show()
def getOverlapSize(frac1, frac2,  cycleOffset1, cycleOffset2):
    end1 = (cycleOffset1 + len(frac1))%lenOfCycle
    if end1 < cycleOffset2:
        val = lenOfCycle - cycleOffset2 + end1
    else:
        val = end1 - cycleOffset2
    return min(val, len(frac1), len(frac2))

def getDistanceBetweenFracs(part1, part2):
    frac1, frac2 = part1[0], part2[0]
    cycleOffset1, cycleOffset2 = part1[1], part2[1]
    if cycleOffset1 + len(frac1) < cycleOffset2:
        print 'np.inf'
        return np.inf
    overLapSize = getOverlapSize(frac1, frac2,  cycleOffset1, cycleOffset2)
    if overLapSize > lenOfCycle or overLapSize > len(frac1) or overLapSize > len(frac2):
        #overLapSize = getOverlapSize(frac1, frac2,  cycleOffset1, cycleOffset2)
        print 'overLapSize > lenOfCycle'
    try:
        return np.mean(np.abs(np.array(frac1[-overLapSize:]) - np.array(frac2[:overLapSize])))
    except:
        print '102'

def appendFracs(part1, part2):
    frac1, frac2 = part1[0], part2[0]
    cycleOffset1, cycleOffset2 = part1[1], part2[1]
    overLapSize = getOverlapSize(frac1, frac2,  cycleOffset1, cycleOffset2)
    overlap = (np.array(frac1[-overLapSize:]) + np.array(frac2[:overLapSize]))/2
    try:
        overlap = overlap.tolist()
        return frac1[:-overLapSize] + overlap + frac2[overLapSize:]
    except:
        pass

whole = qu.orderWithCost(minedParts, getDistanceBetweenFracs, appendFracs)
plt.figure()
plt.plot(whole)
plt.plot(ma.movingAverage(whole, 10, 1.1))

periods =[]
strides = []
stances = []
swings = []
maximaOrder=27
clusteringGranularity=0.5
breaked = prt.breakToPeriods(whole,maximaOrder, clusteringGranularity)
for cycle in breaked:
    if len(cycle)>25 and len(cycle)<60:
        #periods.append(cycle)
        strides.append(cycle)
        min = np.argmin(cycle)
        stances.append(cycle[:min])
        swings.append(cycle[min:])
prt.plotStas(strides, 'Strides')
prt.plotStas(stances, 'stances')
prt.plotStas(swings, 'swings')
"""
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
"""
plt.show()
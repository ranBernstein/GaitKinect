import matplotlib.pyplot as plt
import utils.kinect.angleExtraction as ae
import utils.oldKinectExtractor as ke
import algorithm.stitching as st
import numpy as np
import algorithm.quantization as qu
import utils.utils as pe
import copy
import utils.MovingAverage as ma
import algorithm.partitionizing as prt
from tsp_solver.greedy import solve_tsp
import algorithm.mineByPattern as mp
#Reading from file
fileName = 'myKinect/v2RanLong.skl'
joint = 'KneeLeft_X'
time, frameNumbers, angles= ae.getAngleVec(fileName, joint, True, 'NEW')

#Extracting clean fractions
minimalCluster=20
fracs = ke.clusterByTime(time, frameNumbers, angles, False, minimalCluster)
prob = 0.1
fracs = ke.filterOutliers(fracs, False, prob)
i=0
cleanedParts, _ = ke.cleanFracs(fracs, False, 5, 1.5)
st.plotParts(cleanedParts)

#Creating pattern to mine for
lenOfCycle = 35
pattern = mp.createFlippedUpattern(angles, lenOfCycle, 3)

#Mining the pattern from the input
fig = plt.figure()
framSize= np.ceil(np.sqrt(len(cleanedParts)))
minedParts = []
minedPartsAsList = []
dises = []
threshold = 0
sizeFactor=2
lengths = []
for index, part in enumerate(cleanedParts):
    minimalFracSize = lenOfCycle/2
    retVal = qu.getAtomFromFrac(part, pattern, sizeFactor, minimalFracSize)
    if retVal is None:
        continue
    frac,  dis, vecAtom, bias, bestScale, temporalScale, partOffset,\
        cycleOffset = retVal
    curr = fig.add_subplot(framSize,framSize,index+1)
    plt.title('dis: '+str(dis)+'\n temporalScale: ' + str(temporalScale)+ 
              ',\n scale: '+str(bestScale))
    curr.plot(part, c='b')
    rng = xrange(partOffset, partOffset + len(frac))
    curr.plot(rng, vecAtom, c='g')
    curr.plot(rng, frac, c='r') 
    threshold +=dis
    cycleOffset = cycleOffset%(int(lenOfCycle*temporalScale))
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

def getOverlapSize(frac1, frac2,  cycleOffset1, cycleOffset2, lenOfCycle):
    """
    begin = max(cycleOffset1, cycleOffset2)
    end = min(cycleOffset1+len(frac1), cycleOffset2+len(frac2))
    return (end - begin)%lenOfCycle
    """
    end1 = cycleOffset1+len(frac1)
    end1Index = end1%lenOfCycle
    end2Index = (cycleOffset2 + len(frac2))%lenOfCycle
    if end1Index > end2Index and len(frac2) < lenOfCycle:
        return 0
    if end1Index < cycleOffset2 and len(frac1) < lenOfCycle:
        return 0
    return (end1Index- cycleOffset2)%lenOfCycle

def getDistanceBetweenFracs(part1, part2, lenOfCycle):
    frac1, frac2 = part1[0], part2[0]
    cycleOffset1, cycleOffset2 = part1[1], part2[1]
    if cycleOffset1 + len(frac1) < cycleOffset2:
        return np.inf
    overLapSize = getOverlapSize(frac1, frac2,  cycleOffset1, cycleOffset2, lenOfCycle)
    if overLapSize == 0:
        return np.inf
    if overLapSize > len(frac1) or overLapSize > len(frac2):
        overLapSize = getOverlapSize(frac1, frac2,  cycleOffset1, cycleOffset2, lenOfCycle)
        raise 'overLapSize > frac'
    return np.mean(np.abs(np.array(frac1[-overLapSize:]) - np.array(frac2[:overLapSize])))
    
def appendFracs(part1, part2, lenOfCycle):
    frac1,  frac2 = part1[0], part2[0]
    cycleOffset1, cycleOffset2 = part1[1], part2[1]
    overLapSize = getOverlapSize(frac1, frac2,  cycleOffset1, cycleOffset2, lenOfCycle)
    overlap = (np.array(frac1[-overLapSize:]) + np.array(frac2[:overLapSize]))/2
    overlap = overlap.tolist()
    newFrac = pe.toList(frac1[:-overLapSize]) + overlap + pe.toList(frac2[overLapSize:])
    return (newFrac, cycleOffset1)

mat = []
for p1 in minedParts:
    row=[]
    for p2 in minedParts:
        dis = getDistanceBetweenFracs(p1, p2, lenOfCycle)
        row.append(dis)
    mat.append(row)
print mat
path = solve_tsp( mat )
print path
#whole = qu.orderWithCost(minedParts, getDistanceBetweenFracs, appendFracs)
whole = minedParts[path[0]]
for i in path[1:]:
    whole = appendFracs(whole, minedParts[path[i]], lenOfCycle)
whole = whole[0]
    
plt.figure()
whole = ma.movingAverage(whole, 10, 1.3)
plt.plot(whole)
#plt.plot()
#plt.show()
periods =[]
strides = []
stances = []
swings = []
maximaOrder=15
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
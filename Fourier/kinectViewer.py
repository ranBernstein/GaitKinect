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

fileName = 'myKinect/y1.skl'
joint = 'KneeLeft_X'
time, angles= ae.getAngleVec(fileName, joint, True)

#Extracting clean fractions
minimalCluster=20
fracs = ke.clusterByTime(time, angles, False, minimalCluster)
prob = 0.1
fracs = ke.filterOutliers(fracs, False, prob)
i=0
cleanedParts, _ = ke.cleanFracs(fracs, False, 20, 1.1)
st.plotParts(cleanedParts)

#Creating pattern to mine for
up = np.linspace(40, 70, 20)
start = 20
end = 45
up = (np.linspace(start,end,15)).tolist()
down = list(reversed(up))
pattern = [start, start, start] + up + ([end]*5) + down + [start, start, start]
plt.figure()
plt.plot(pattern)
fig = plt.figure()
framSize= np.ceil(np.sqrt(len(cleanedParts)))
minedParts = []
minedPartsAsList = []
dises = []
threshold = 0

#cleanedParts = cleanedParts[:3]
lengths = []
for index, part in enumerate(cleanedParts):
    retVal = qu.getAtomFromFrac(part, pattern, qu.extractPartialPattern)
    if retVal is None:
        continue
    frac,  dis, vecAtom, bias, bestScale, temporalScale, partOffset,\
        cycleOffset = retVal
    curr = fig.add_subplot(framSize,framSize,index+1)
    plt.title('dis: '+str(dis)+'\n temporalScale: ' + str(temporalScale)+ 
              ',\n scale: '+str(bestScale))
    #plt.ylim((0,50))
    curr.plot(part, c='b')
    rng = xrange(partOffset, partOffset + len(frac))
    curr.plot(rng, vecAtom, c='g')
    curr.plot(rng, frac, c='r') 
    threshold +=dis
    minedParts.append((frac, cycleOffset, [i]))
    minedPartsAsList.append(frac)
    dises.append(dis)
    lengths.append(len(frac))
st.plotParts(minedPartsAsList)

#threshold/=len(cleanedParts)
threshold = np.percentile(dises, 60)
#minedPartsAsListCopy = copy.deepcopy(minedPartsAsList)
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

whole = qu.orderWithCost(minedPartsAsList)
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
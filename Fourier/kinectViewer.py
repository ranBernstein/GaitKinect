import matplotlib.pyplot as plt
import utils.angleExtraction as ae
import utils.oldKinectExtractor as ke
import utils.stitching as st
import numpy as np
import utils.quantization as qu

fileName = 'myKinect/y1.skl'
joint = 'KneeLeft_X'
time, angles= ae.getAngleVec(fileName, joint, True)
minimalCluster=20
fracs = ke.clusterByTime(time, angles, False, minimalCluster)
prob = 0.1
#fracs = ke.filterOutliers(fracs, False, prob)
i=0
cleanedParts, kuku = ke.cleanFracs(fracs, False, 20, 1.1)
up = np.linspace(40, 70, 20)
start = 20
end = 45
up = (np.linspace(start,end,15)).tolist()
down = list(reversed(up))
pattern = [end, end] + down + ([start]*5) + up + [end, end]
fig = plt.figure()
framSize= np.ceil(np.sqrt(len(cleanedParts)))
for part in cleanedParts:
    retVal = qu.getAtomFromFrac(part, pattern, qu.extractPartialPattern)
    if retVal is None:
        continue
    frac,  dis, vecAtom, bias, bestScale, temporalScale, partOffset,\
        cycleOffset = retVal
    curr = fig.add_subplot(framSize,framSize,index)
st.plotParts(cleanedParts)
#plt.scatter(time, angles)
plt.show()
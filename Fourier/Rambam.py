import utils.angleExtraction as ae
import matplotlib.pyplot as plt
import utils.oldKinectExtractor as ke
import utils.quantization as qu
import utils.stitching as st


atoms = [
             [14, 15, 17, 19, 24, 28, 33, 33, 33, 33],
             [33, 33, 33, 33, 28, 24, 19, 17, 15, 14],
             [15, 14, 12, 12, 14, 15, 16, 17.5, 17.5, 17.5],
             [17.5, 17.5, 16, 15, 14, 13, 12, 12, 14, 15]
        ]

fileName = 'inputs/Rambam/4984982498.skl'
joint = 'AnkleRight_X'
time, angles= ae.getAngleVec(fileName, joint, True)
subject=[]
#seperators = [1210, 2371, 4017, len(time)]  
seperators = [8466828, 8703358, 9942719, 10363068]  
subjects = []
sizeOfAtom = 10
minimalCluster = sizeOfAtom
start =0 
for end in seperators:
    tmpTime = []
    tmpAngles = []
    for t, a in zip(time, angles):
        if t > start and t < end:
            tmpTime.append(t)
            tmpAngles.append(a) 
    plt.figure()
    plt.plot(tmpTime, tmpAngles)
    fracs = ke.clusterByTime(tmpTime, tmpAngles, False, minimalCluster)
    prob = 0.3
    fracs = ke.filterOutliers(fracs, False, prob)
    cleanedParts, kuku = ke.cleanFracs(fracs, False)
    st.plotParts(cleanedParts, 'Frames', 'Knee angle', xrange(len(cleanedParts)), (0,100), (0,45))
    start = end
    subjects.append(fracs)
#plt.plot(time, angles)
#for s in subjects:
    
"""
minimalCluster=15
fracs = ke.clusterByTime(time, angles, False, minimalCluster)
prob = 0.3
fracs = ke.filterOutliers(fracs, False, prob)
cleanedParts, kuku = ke.cleanFracs(fracs, False)
#angles = [item for sublist in cleanedParts for item in sublist]
#bins = qu.getEquallyWeighetedBins(angles, alphabetSize)

#wholeStr = qu.createStr(bins, angles)
#vec = qu.fromStr2Vec(bins, wholeStr)
#ngrams_statistics_sorted = qu.getSortedNgrams(wholeStr, n)
atoms = [
             [14, 15, 17, 19, 24, 28, 33, 33, 33, 33],
             [33, 33, 33, 33, 28, 24, 19, 17, 15, 14],
             [15, 14, 12, 12, 14, 15, 16, 17.5, 17.5, 17.5],
             [17.5, 17.5, 16, 15, 14, 13, 12, 12, 14, 15]
        ]
lot(str)
alphabetSize = 10
sizeOfAtom=10
radius=2
numOfClusters=20
vecs, mats = qu.createClustersAndMatchingMatrices(cleanedParts, atoms, radius, sizeOfAtom, 
                                               alphabetSize, numOfClusters)
       
strides = qu.createStridesFromAtoms(mats, vecs)
st.plotParts(strides)

#whole = qu.orderWithCost(strides)
#plt.figure()
#plt.plot(whole)
"""
plt.show()
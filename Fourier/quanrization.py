import utils.angleExtraction as ae
import matplotlib.pyplot as plt
import utils.oldKinectExtractor as ke
import utils.quantization as qu
import utils.stitching as st



fileName = 'inputs/ran_5_2_14_840.skl'#asc_gyro_l.skl'
joint = 'AnkleRight_X'
time, angles, kuku = ae.getAngleVec(fileName, joint, False)
#plt.plot(angles)
minimalCluster=15
fracs = ke.clusterByTime(time, angles, False, minimalCluster)
prob = 0.3
fracs = ke.filterOutliers(fracs, False, prob)
cleanedParts, kuku = ke.cleanFracs(fracs, False)
angles = [item for sublist in cleanedParts for item in sublist]
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
"""
str = qu.appendAtom(atoms[0], atoms[1])
str = qu.appendAtom(str, atoms[2])
str = qu.appendAtom(str, atoms[3])
plt.plot(str)
"""
alphabetSize = 10
sizeOfAtom=10
#radius=2
numOfClusters=12
disFactor = 0.1
vecs, mats = qu.createClustersAndMatchingMatrices(cleanedParts, atoms, 
                                    numOfClusters, disFactor)
       
strides = qu.createStridesFromAtoms(mats, vecs)
st.plotParts(strides)
plt.show()
whole = qu.orderWithCost(strides)
plt.figure()
plt.plot(whole)

plt.show()








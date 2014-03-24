import utils.angleExtraction as ae
import matplotlib.pyplot as plt
import utils.oldKinectExtractor as ke
import utils.quantization as qu
import utils.stitching as st
import math
import numpy as np
import copy
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
#end = 8466828
    tmpTime = []
    tmpAngles = []
    for t, a in zip(time, angles):
        if t > start and t < end:
            tmpTime.append(t)
            tmpAngles.append(a) 
    start = end
    
    fracs = ke.clusterByTime(tmpTime, tmpAngles, False, minimalCluster)
    originalFracs = copy.deepcopy(fracs)
    prob = 0.05
    fracs = ke.filterOutliers(fracs, False, prob)
    i=0
    cleanedParts, kuku = ke.cleanFracs(fracs, False)
    """
    for (t, a), part in zip(originalFracs,cleanedParts):
        frameSize = math.ceil(np.sqrt(len(fracs)))
        curr = fig.add_subplot(frameSize,frameSize,i+1)
        plt.title(str(i))
        plt.xlabel('Time in miliseconds')
        plt.ylabel('Right knee angle in degrees')
        curr.plot(xrange(len(a)), a, c='b')
        curr.plot(part, c='g')
        i+=1
    st.plotParts(cleanedParts, 'Frames', 'Knee angle', xrange(len(cleanedParts)))#, (0,100), (0,45))
    """
    alphabetSize = 10
    sizeOfAtom=10
    radius=2
    numOfClusters=2
    vecs, mats = qu.createClustersAndMatchingMatrices(cleanedParts, atoms, radius, sizeOfAtom, 
                                              alphabetSize, numOfClusters)
    strides = qu.createStridesFromAtoms(mats, vecs)
    xlabel = 'Frames(each frame is 33 miliseconds)'
    ylabel = 'Right knee angle (in degrees)'
    #st.plotParts(strides, xlabel, ylabel, xrange(len(strides)))
    if(numOfClusters > 2):
        whole = qu.orderWithCost(strides)
    else: 
        if(numOfClusters == 2) :
            byOrderDis = qu.getDistanceBetweenAtoms(strides[0], strides[1])
            byOrder = qu.appendAtom(strides[0], strides[1])
            inverseDis = qu.getDistanceBetweenAtoms(strides[1], strides[0])
            inverse = qu.appendAtom(strides[1], strides[0])
            whole = byOrder if byOrderDis < inverseDis else inverse
        else:
            whole = strides[0]
    plt.figure()
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.plot(whole)
plt.show()
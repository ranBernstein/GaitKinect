import utils.oldKinectExtractor as ex
import utils.kinect.angleExtraction as ae
import matplotlib.pyplot as plt
import utils.stitching.stitching as loop

fileName = 'inputs/asc_gyro_l.skl'#alon_multi_right.skl
joint = 'AnkleRight_X'
time, angles = ae.getAngleVec(fileName, joint, True)
startGrade=0.93
minimalOverlap=10
maximalOverlap=200
lengthFactor=0
density = 2
parts, stitchedParts, partDescriptors = ex.stitchByDensity(time, angles, False, 
   startGrade, minimalOverlap, maximalOverlap, lengthFactor, density)
for des in partDescriptors:
    loop.plotDes(parts, des)
minimalOverlap=5
maximalOverlap=15
density = 5
stitchedParts, partDescriptors = loop.stitch(stitchedParts, startGrade, minimalOverlap, \
                                         maximalOverlap, lengthFactor, density)
for des in partDescriptors:
    loop.plotDes(parts, des)
"""
fracs = ex.clusterByTime(time, angles, False)
fracs = ex.filterOutliers(fracs, False)   
cleanedParts, originalParts = ex.cleanFracs(fracs, False)
parts, partDescriptors = loop.stitch(cleanedParts, startGrade, minimalOverlap, \
    maximalOverlap, lengthFactor, density)
"""
plt.figure()
plt.plot(stitchedParts[-1])
plt.show()
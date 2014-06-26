import utils.kinect.angleExtraction as ae
import utils.stitching.stitching.quantization as qu
import matplotlib.pyplot as plt

fileName = 'inputs/ran_5_2_14_840.skl'
joint = 'AnkleRight_X'
time, angles = ae.getAngleVec(fileName, joint, True)
disFactor=0.05
numOfClusters = 12
res = qu.doRambamAlgo(time, angles, numOfClusters, disFactor)
plt.figure()
plt.plot(res)
plt.show()
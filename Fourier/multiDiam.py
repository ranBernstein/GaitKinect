import utils.angleExtraction as ae
import utils.quantization as qu
import matplotlib.pyplot as plt

fileName = 'inputs/ran_5_2_14_840.skl'
joint = 'AnkleRight_X'
time, angles = ae.getAngleVec(fileName, joint, True)
disFactor=0.2
res = qu.doRambamAlgo(time, angles, disFactor)
plt.plot(res)
plt.show()
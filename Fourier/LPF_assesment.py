import numpy as np
from utils.stitching import MAXIMA_ORDER, CLUSTER_COEFF, plotParts, createParts
import utils.stitchingLoop as loop 
import utils.periodAnalysisUtils as ut
from operator import add, sub
import utils.LPF as LPF 
import numpy.random as rnd
import matplotlib.pyplot as plt 
from utils.amcParser import getAMCperiod

def mse(A, B):
    return ((np.array(A) - np.array(B)) ** 2).mean(axis=0)
def me(A, B):
    return np.mean([np.abs(x-y) for x, y in zip(A,B)])

file = 'AMCs/598.amc'
joint = 'rtibia'
list = getAMCperiod(joint, file)
stride = list[112:251] 
list = ut.alignByMax(stride)
amplitude = np.max(list) - np.min(list)
coeffs_nums = xrange(1, len(list)/4)
def checkNoise(noiseFactor):
    mses = []
    noises = []
    for coeffs_num in coeffs_nums:
        sums = []
        for i in xrange(30):
            noise = map(add, np.random.normal(0,(amplitude/noiseFactor)**2,len(list)), list)
            clean = LPF.clean(noise, coeffs_num)
            sums.append(me(list, clean))
            noises.append(me(list, noise))
        mses.append(np.mean(sums))
    plt.plot(coeffs_nums, mses, label='amplitude/noise_std=' + str(factor))
    m = np.mean(noises)
    plt.plot(coeffs_nums, [m]*len(coeffs_nums), label='noise reference for ' + str(factor))
factors = [4,6, 8]
for factor in factors:
    checkNoise(factor)
#plt.plot(list, c='b')
#plt.plot(ma, c='g')
#plt.plot(noise, c='r')
#plt.plot(LPFed, c='black')
plt.xlabel('coeffs num')
plt.ylabel('me')
plt.title('Mean error as function of coeffs num of different noises')
plt.legend().draggable()
plt.show()
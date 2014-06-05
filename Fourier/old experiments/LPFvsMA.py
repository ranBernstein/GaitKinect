import numpy as np
from utils.stitching.stitching import MAXIMA_ORDER, CLUSTER_COEFF, plotParts, createParts
import utils.stitching.stitching as loop
import utils.periodAnalysisUtils as ut
from operator import add, sub
import utils.LPF as LPF 
import numpy.random as rnd
import matplotlib.pyplot as plt 
from utils.vicon.amcParser import getAMCperiod
from utils.MovingAverage import movingAverage
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
coeffs_num = 16
window_size = 16
maFactor = 1.2
msesMA = []
msesLPF = []
noises = []
noisesFactors = xrange(2,20)
for noiseFactor in noisesFactors:
    sumsLPF = []
    sumsMA = []
    sumsN = []
    for i in xrange(30):
        noise = map(add, np.random.normal(0,(amplitude/noiseFactor)**2,len(list)), list)
        clean = LPF.clean(noise, coeffs_num)
        ma = movingAverage(noise,  window_size, maFactor)
        sumsLPF.append(me(list, clean))
        sumsMA.append(me(list, ma))
        sumsN.append(me(list, noise))
    msesMA.append(np.mean(sumsMA))
    msesLPF.append(np.mean(sumsLPF))
    noises.append(np.mean(sumsN))
plt.plot(noisesFactors, msesMA, label='MA' )
plt.plot(noisesFactors, msesLPF, label='LPF' )
plt.plot(noisesFactors, noises, label='noise reference for ')

plt.xlabel('noises factors')
plt.ylabel('me')
plt.title('Mean error of different noises')
plt.legend().draggable()
plt.show()
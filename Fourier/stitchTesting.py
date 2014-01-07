import numpy as np
import numpy.random as rnd
import matplotlib.pyplot as plt 
from utils.amcParser import getAMCperiod
from utils.stitching import MAXIMA_ORDER, CLUSTER_COEFF, plotParts, createParts
import utils.stitchingLoop as loop 
import utils.periodAnalysisUtils as ut
from operator import add, sub
import utils.LPF as LPF 

file = 'AMCs/598.amc'
joint = 'rtibia'
list = getAMCperiod(joint, file)
stride = list[112:251] 
list = ut.alignByMax(stride)
#list = ut.alignByMax(list)
parts = createParts(list, True, 9, 5)
merged = loop.stitch(parts)
merged.sort()
print(len(merged))
out = ut.alignByMax(merged[-1])
plt.figure()
plt.plot(out, color='r')
out = LPF.clean(out) 
plt.plot(list, color='b')
plt.plot(out, color='g')
plt.show()


"""
stride = list[112:251] 
stride = ut.alignByMax(stride)
noiseVar = 12
frac1 = stride[:100]
frac1 = map(add, np.random.normal(0,noiseVar,len(frac1)), frac1)
plt.figure()
plt.plot(frac1)
frac1 = LPF.clean(frac1)
frac2 = stride[70:]
frac2 = map(add, np.random.normal(0,noiseVar,len(frac2)), frac2)
plt.figure()
plt.plot(frac2)
frac2 = LPF.clean(frac2)
"""
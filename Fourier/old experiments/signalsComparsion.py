import numpy as np
import numpy.random as rnd
import matplotlib.pyplot as plt 
from utils.vicon.amcParser import getAMCperiod
from utils.stitching.stitching import MAXIMA_ORDER, CLUSTER_COEFF, plotParts, createParts
import utils.stitching.stitching as loop
import utils.periodAnalysisUtils as ut
from operator import add, sub
import utils.LPF as LPF 

file = 'AMCs/598.amc'
joint = 'root'
list = getAMCperiod(joint, file)
list = list[:538]
#stride = list[112:251] 
#list = ut.alignByMax(stride)
#list = ut.alignByMax(list)
amplitude = np.max(list) - np.min(list)
parts = createParts(list, True, 9, amplitude/10)
merged = loop.stitch(parts)
merged.sort()
print(len(merged))
#out = ut.alignByMax(merged[-1])
out = LPF.clean(merged[-1]) 
outOff, listOff = ut.alignByBig(out, list)
plt.figure()
plt.plot(xrange(listOff, listOff+len(list)), list)
plt.plot(xrange(outOff, outOff+len(out)), out)
plt.show()
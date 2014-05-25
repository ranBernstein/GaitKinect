import numpy as np
import numpy.random as rnd
import matplotlib.pyplot as plt 
from utils.amcParser import getAMCperiod
from utils.stitching import MAXIMA_ORDER, CLUSTER_COEFF, plotParts, createParts
import utils.stitchingLoop as loop 
import utils.periodAnalysisUtils as ut
from operator import add, sub
import utils.LPF as LPF 

file = '../AMCs/subjects/5/origin.amc'
joint = 'rtibia'
list = getAMCperiod(joint, file)
plt.plot(list)
plt.show()
import Cleaner
from jointsMap import Joints
import matplotlib.pyplot as plt
import math
import numpy as np
import LPF
import periodAnalysisUtils

file = 'inputs/assaf_45.skl'
joint = Joints.KneeLeft_X
#Cleaner.plotJointCentered(file, joint)
parts = Cleaner.plotJointCenteredPeriodicaly(file, joint)
dirty_fig = plt.figure()
without_outliers_fig = plt.figure()
clean_fig = plt.figure()
clean_and_wo = plt.figure()
for part in parts:
    frameSize = math.ceil(np.sqrt(len(parts)))
    dirty_sub = dirty_fig.add_subplot(frameSize*110 + parts.index(part)+1)
    time = zip(*part)[0]
    values = zip(*part)[1]
    dirty_sub.plot(time, values)
    
    dropped_values, dropped_time = periodAnalysisUtils.dropOutliers(values, time)
    wo_sub = without_outliers_fig.add_subplot(frameSize*110 + parts.index(part)+1)
    wo_sub.plot(dropped_time, dropped_values)
    
    clean_values, clean_time =  LPF.clean(values, time)
    clean_sub = clean_fig.add_subplot(frameSize*110 + parts.index(part)+1)
    clean_sub.plot(clean_time, clean_values)
    
    cAw_v, cAw_t =  LPF.clean(dropped_values, dropped_time)
    cleanAw_sub = clean_and_wo.add_subplot(frameSize*110 + parts.index(part)+1)
    cleanAw_sub.plot(clean_time, clean_values)
    
plt.show()
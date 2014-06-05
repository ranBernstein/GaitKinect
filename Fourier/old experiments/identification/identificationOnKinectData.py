import utils.angleExtraction as ae
import matplotlib.pyplot as plt
import utils.stitching.stitching.partitionizing as pa
import utils.misc.animate as an
import utils.oldKinectExtractor as ex
from utils.stitching.stitching import plotParts
from sklearn.neighbors import KNeighborsClassifier
from utils.misc import crossValidate.crossValidate
import utils.interpulation as inter
import numpy as np
joint = 'AnkleRight_X'
files = {}
subjects = ['mickey', 'alon', 'assaf', 'tal', 'yoko', 'micha', 'asc', 'pd']
multiList = ['micky', 'alon', 'assaf']
singleList = ['micha']
noisyList = ['tal', 'yoko', 'asc']
#files['micha']  = ['inputs/micha_walk_45.skl', 'inputs/micha_walk.skl']
#files['tal'] = ['inputs/tal_l2r.skl', 'inputs/tal_r2l.skl']
#files['yoko'] = ['inputs/yoko.skl']
#files['alon'] = ['inputs/alon_multi_right.skl', 'inputs/alon_multi_left.skl']
#files['assaf'] = ['inputs/assaf_45.skl']
files['asc'] = ['inputs/asc_gyro_l.skl']#, 'inputs/asc_gyro_r.skl']
#files['mickey'] = ['inputs/mickey_multi_left.skl', 'inputs/mickey_multi_right.skl']#, 'inputs/mickey_multi_120cm_right.skl']
#files['pd'] = ['inputs/pd_1_a.skl']#, 'inputs/pd_1_a.skl']

def srtridesFromKinectFile(fileName, joint, plot=False):
    time, angles, weights = ae.getAngleVec(fileName, joint, False)
    stitched = ex.stitchKinect(time, angles, weights, plot)
    periods = pa.breakToPeriods(stitched)
    if(plot):
        plt.figure()
        plt.title(fileName)
        plt.plot(stitched)
        plotParts(periods)
    return periods
samples = []
tags = []

for subject, records in files.items():
    for file in records:
        periods = srtridesFromKinectFile(file, joint, True)
        periods = inter.getUniformSampledVecs(periods, 50)
        samples = samples + periods
        tags = tags + [subjects.index(subject)]*len(periods)

"""
cl = KNeighborsClassifier()
cl.n_neighbors = 1
cl.weights = 'distance' 
scores = []
for i in xrange(len(samples)):
    cl.fit(samples[:i] + samples[i+1:], tags[:i] + tags[i+1:])
    scores.append(cl.score([samples[i]], [tags[i]]))
print len(samples)
print np.mean(scores)
"""
plt.show()
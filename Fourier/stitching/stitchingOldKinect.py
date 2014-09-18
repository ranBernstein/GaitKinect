import utils.kinect.angleExtraction as ae
import matplotlib.pyplot as plt
import utils.oldKinectExtractor as ex
import itertools
import numpy as np
fileName = 'inputs/alon_multi_right.skl'#'inputs/asc_gyro_l.skl'
joint = 'AnkleRight_X'


time, angles, weights = ae.getAngleVec(fileName, joint, False)
startGrade=0.93
minimalOverlap=10
maximalOverlap=50
lengthFactor=0#-0.4
merged, des, fracs = ex.stitchKinect(time, angles, weights, True, startGrade,
                         minimalOverlap, maximalOverlap, lengthFactor)

time, values = zip(*fracs)
sortingIndices = sorted(des.keys(), key=lambda k: des[k][0])
timeLine = []
for i in sortingIndices:
    timeLine = timeLine[:des[i][0]] + time[i]
#timeLine = list(itertools.chain(*time))

mat = {}
file = open(fileName, 'r')
headersStr = file.readline()
headers = headersStr.split()
for line in file:
    splited = line.split()
    mat[float(splited[0])] = splited[1:]
#mat = mat[timeLine]
#mat = {k: mat[k] for k in timeLine}
bestFeatures = open('bestFeatures.skl', 'w')
bestFeatures.flush()
bestFeatures.write(headersStr)
#bestFeatures.write(headers)
lastT = timeLine[0]
lastNewT = lastT
lastValues = {}
lastNewValues = {}
headersWOtime = headers[1:]
for header in xrange(len(headersWOtime)):
    x = float(mat[timeLine[0]][header]) 
    lastValues[header] = x
    lastNewValues[header] = x
frameNum = 0
newData = []
for t in timeLine:
    delta = np.abs(t - lastT)
    lastT = t
    line = mat[t]
    newT = lastNewT + delta if delta < ex.MAXIMAL_TIME_GAP else lastNewT + 33
    bestFeatures.write(str(newT) + '\t')
    lastNewT = newT
    #newStr = str(newT) + '\t'
    splited = [newT]
    off = {}
    off['X'] = float(line[headersWOtime.index('HipCenter_X')]) 
    off['Y'] = float(line[headersWOtime.index('HipCenter_Y')]) - 1
    off['Z'] = float(line[headersWOtime.index('HipCenter_Z')]) - 2
    for i,header in enumerate(headersWOtime):
        #deltaV = 0
        #if(delta < ex.MAXIMAL_TIME_GAP):
            #deltaV = float(line[i]) - lastValues[i]
        #newV = lastNewValues[i] + deltaV
        suf = header[-1] 
        newV = float(line[i]) - off.get(suf, 0)
        #lastNewValues[i] = newV
        #lastValues[i] = float(line[i])
        if(header == 'framenum'):
            newV = frameNum
        else: 
            if 'tracked' in header:
                newV = 2
        bestFeatures.write(str(newV) + '\t')
    bestFeatures.write('\n')
    frameNum += 1
bestFeatures.close()         
print 'end' 
plt.show()










import numpy as np
import sys
from math import sqrt, acos
from jointsMap import ancestorMap, Joints
import matplotlib.pyplot as plt



def getAnccestorRelativePos(splited, isRelative, chosenIndices):
    input = []
    for i in range(len(splited)):
        if chosenIndices and i not in chosenIndices:
            continue
        try:
            anc = ancestorMap[i]
            trackedValue = int(splited[(i+1)-(i+1)%4 + 2])
            if(trackedValue == 0):
                return []
            pos = splited[i]
            if(isRelative):
                pos = float(splited[i]) - float(splited[anc])                  
            input.append(pos)
        except:
            if(i>6 and i%4!=2):
                pos = splited[i]
                input.append(pos)
            continue
    return input
#normalize vector between 0 to 1
def normelizeVector(vec):
    if(len(vec)==0):
        raise BaseException('normelizeVector got empty vec')
    arr = np.array(vec)
    arr = [float(f) for f in arr]
    mean = np.mean(arr)
    arr = [x - mean for x in arr]
    ma = np.amax(arr)
    mi = np.amin(arr)
    length = max(abs(ma), abs(mi)) *2
    arr = [x/length + 0.5 for x in arr]
    return arr

def normelizeInput(x):
    x = np.array(x)
    diam = len(np.shape(x))
    if(diam == 1):
        x = np.reshape(x, (len(x), 1))
    
    numOfSamples, numOfFeatures = np.shape(x)
    newX = np.empty((numOfSamples, 0))
    for i in xrange(numOfFeatures):
        vec = x[:,i]
        vec = normelizeVector(vec)
        vec = np.reshape(vec, (len(vec),1))
        newX = np.concatenate((newX, vec), axis=1)
    return newX

def dotproduct(v1,v2):
    return sum((a*b) for a, b in zip(v1, v2))

def length(v):
    return sqrt(dotproduct(v, v))

def angle(v1, v2):
    return acos(dotproduct(v1, v2) / (length(v1) * length(v2)))

def calcAngle(x1, y1, z1, x2, y2, z2, x3, y3, z3):
    v1 = [x1-x2, y1-y2, z1-z2]
    v2 = [x3-x2, y3-y2, z3-z2]
    return angle(v1,v2)

def dis(x1, x2, y1, y2, z1, z2):
    return sqrt((x1-x2)**2 + (y1-y2)**2 + (z1-z2)**2)

def prepareAnglesFromInput(filePath, i, outputIndex, check, allByTime, allByJoint):
    f = open(filePath, 'r')
    headers = f.readline().split()
    output = []
    time = [] 
    for line in f:
        splited = line.split() 
        timeStamp = int(splited[0])
        splited = np.array(splited)
        try:
            x = float(splited[i])
            y = float(splited[i+1])
            z = float(splited[i+2])
            tracked = int(splited[i+3])
            fatherIndex_x = ancestorMap[i]
            father_x = float(splited[fatherIndex_x])
            father_y = float(splited[fatherIndex_x+1])
            father_z = float(splited[fatherIndex_x+2])
            father_tracked = int(splited[fatherIndex_x+3])
            grandFatherIndex_x =  ancestorMap[fatherIndex_x]
            grandFather_x = float(splited[grandFatherIndex_x])
            grandFather_y = float(splited[grandFatherIndex_x+1])
            grandFather_z = float(splited[grandFatherIndex_x+2])
            grandFather_tracked = int(splited[grandFatherIndex_x+3])
            if(check and (tracked != 2 or father_tracked != 2 or grandFather_tracked != 2)):
                raise '0 value feature'                     
            angle = calcAngle(x, y, z, father_x,father_y,father_z, grandFather_x,grandFather_y,grandFather_z)
        except:
            #print "Unexpected error:", sys.exc_info()[0]
            continue
        output = float(splited[outputIndex])
        allByTime[timeStamp]['output'] = output
        allByTime[timeStamp][i] = angle
        allByJoint[i][timeStamp] = angle
        time.append(int(splited[0]))
    f.close()
    return allByTime, allByJoint
"""   
time, res = prepareAnglesFromInput('asc_gyro_l.skl', [63])
plt.scatter(time,res)
print len(res)
plt.show()
"""










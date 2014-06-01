import numpy as np
import sys
from math import sqrt, acos
from jointsMap import ancestorMap
from periodAnalysisUtils import binaryByMean, binaryByMedian, deriveTimeSeries, smoothOutliers

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
    inRad = acos(dotproduct(v1, v2) / (length(v1) * length(v2)))
    return inRad*180.0/np.pi

def createVectors(x1, y1, z1, x2, y2, z2, x3, y3, z3):
    return [x2-x3, y2-y3, z2-z3], [x1-x2, y1-y2, z1-z2]

def calcAngle(x1, y1, z1, x2, y2, z2, x3, y3, z3):
    v1, v2 = createVectors(x1, y1, z1, x2, y2, z2, x3, y3, z3)
    return angle(v1,v2)

def dis(x1, x2, y1, y2, z1, z2):
    return sqrt((x1-x2)**2 + (y1-y2)**2 + (z1-z2)**2)

def fromIndex2Point(line, i):
    return line[i], line[i+1], line[i+2]
 
def calcDisFromIndices(line, i1, i2):
    return dis(line[i1], line[i2], line[i1+1], line[i2+1], line[i1+2], line[i2+2])

def calcJointsAverage(line, jointsIndices):
    xSum, ySum, zSum = 0,0,0
    for i in jointsIndices:
        xSum, ySum, zSum = xSum+line[i], ySum+line[i+1], zSum+line[i+2]
    xSum, ySum, zSum = xSum/len(jointsIndices), ySum/len(jointsIndices), zSum/len(jointsIndices)
    return xSum, ySum, zSum

def calcAverageDistanceOfIndicesFromPoint(line, jointsIndices,px,py,pz):
    sum=0
    for i in jointsIndices:
        sum+= dis(px, line[i],py, line[i+1],pz, line[i+2])
    return sum/len(jointsIndices)

def calcAverageJointDistanceFromCenter(line, jointsIndices):
    center = calcJointsAverage(line, jointsIndices)
    return calcAverageDistanceOfIndicesFromPoint(line, jointsIndices,*center)

def distancePointLine (px, py, pz, x1, y1, z1, x2, y2, z2):
    lineMag = length([x2-x1,y2- y1,z2- z1])
    u = ((px - x1) * (x2 - x1)) + ((py - y1) * (y2 - y1)) + ((pz - z1) * (z2 - z1))
    u = u / (lineMag * lineMag)
    ix = x1 + u * (x2 - x1)
    iy = y1 + u * (y2 - y1)
    iz = z1 + u * (z2 - z1)
    return length([px-ix, py-iy, pz-iz])

def getDisFromAxeByIndecies(line, pointIndex, axeIndex1, axeIndex2):
    return distancePointLine(line[pointIndex], line[pointIndex+1], line[pointIndex+2], \
                             line[axeIndex1],line[axeIndex1+1],line[axeIndex1+2], \
                             line[axeIndex2],line[axeIndex2+1],line[axeIndex2+2])
    
def calcAverageDistanceOfIndicesFromLine(line, jointsIndices,axeIndex1, axeIndex2):
    sum=0
    for i in jointsIndices:
        sum+= getDisFromAxeByIndecies(line, i, axeIndex1, axeIndex2)
    return sum/len(jointsIndices)

def getAngleFromSplited(headers, splited, jointStr, checkConfedence=True, version='OLD'):
    jointCol = headers.index(jointStr)
    x = float(splited[jointCol])
    y = float(splited[jointCol+1])
    z = float(splited[jointCol+2])
    tracked = int(splited[jointCol+3])
    fatherStr = ancestorMap[version][jointStr]
    fatherIndex_x = headers.index(fatherStr)
    father_x = float(splited[fatherIndex_x])
    father_y = float(splited[fatherIndex_x+1])
    father_z = float(splited[fatherIndex_x+2])
    father_tracked = int(splited[fatherIndex_x+3])
    grandFatherIndex_x =  headers.index(ancestorMap[version][fatherStr])
    grandFather_x = float(splited[grandFatherIndex_x])
    grandFather_y = float(splited[grandFatherIndex_x+1])
    grandFather_z = float(splited[grandFatherIndex_x+2])
    grandFather_tracked = int(splited[grandFatherIndex_x+3])
    if(checkConfedence and (tracked != 2 or father_tracked != 2 or grandFather_tracked != 2)):
        return None
    v1, v2 = createVectors(x, y, z, father_x,father_y,father_z, grandFather_x,grandFather_y,grandFather_z)
    if(length(v1) == 0 or length(v2) == 0):
        return None
    a = angle(v1, v2)
    weight = tracked + father_tracked + grandFather_tracked
    retVal = a if checkConfedence else (a, weight)
    return retVal

#for the Vicon
def getAngleByColumns(splited, headers, fatherStr, midStr, childStr):
    fatherCol = headers.index(fatherStr)
    midCol = headers.index(midStr)
    childCol = headers.index(childStr)
    try:
        #print 'kuku:', splited[childCol]
        x = float(splited[childCol])
        y = float(splited[childCol+1])
        z = float(splited[childCol+2])
        father_x = float(splited[midCol])
        father_y = float(splited[midCol+1])
        father_z = float(splited[midCol+2])
        grandFather_x = float(splited[fatherCol])
        grandFather_y = float(splited[fatherCol+1])
        grandFather_z = float(splited[fatherCol+2])
        v1, v2 = createVectors(x, y, z, father_x,father_y,father_z, grandFather_x,grandFather_y,grandFather_z)
        if(length(v1) == 0 or length(v2) == 0):
            return None
        a = angle(v1, v2)
        return a
    except Exception, e:
        return None

def getAngleVec(filePath, jointStr, checkConfedence=True, version='OLD'):
    f = open(filePath, 'r')
    headers = f.readline().split()
    time = []
    frameNumbers = []
    angles = []
    weights = []
    for line in f:
        splited = line.split() 
        timeStamp = int(splited[headers.index('timestamp')])
        frameNum = int(splited[headers.index('framenum')])
        splited = np.array(splited)
        retVal = getAngleFromSplited(headers, splited, jointStr, checkConfedence, version)
        if(retVal is None):
            continue
        weight = None
        if(checkConfedence):
            angle = retVal
        else:
            angle, weight = retVal
        time.append(timeStamp)
        frameNumbers.append(frameNum)
        angles.append(angle)
        if(weight is not None):
            weights.append(weight)
    retVal = (time, frameNumbers, angles) if checkConfedence else \
        (time, frameNumbers, angles, weights)
    return retVal

def prepareAnglesFromInput(filePath, i, outputIndex, check, allByTime, allByJoint):
    f = open(filePath, 'r')
    headers = f.readline().split()
    output = []
    time = [] 
    for line in f:
        splited = line.split() 
        timeStamp = int(splited[0])
        splited = np.array(splited)
        output = float(splited[outputIndex])
        if(output == 0):
            continue
        allByTime[timeStamp]['output'] = output
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
            #if(check and (tracked == 0 or father_tracked == 0 or grandFather_tracked == 0)):
                raise '0 value feature'                     
            angle = calcAngle(x, y, z, father_x,father_y,father_z, grandFather_x,grandFather_y,grandFather_z)
        except:
            continue
        allByTime[timeStamp][i] = angle
        allByJoint[i][timeStamp] = angle
    f.close()
    
    return allByTime, allByJoint

def prepareAngularVelocityFromInput(filePath, i, outputIndex, check, allByTime, allByJoint):
    allByTime, allByJoint = prepareAnglesFromInput(filePath, i, outputIndex, True, allByTime, allByJoint)
    time = allByJoint[i].keys()
    time.sort()
    values = []
    tmpTime = []
    for t in time:
        values.append(allByJoint[i][t])
        tmpTime.append(t)
    time = tmpTime
    plt.plot(time,values)
    values = binaryByMedian(values)
    values = smoothOutliers(values)
    plt.plot(time,values)
    time, derived = deriveTimeSeries(time, values)
    binaryDerived = binaryByMedian(derived)
            
    #plt.plot(time,binaryDerived)
    plt.show()
    return time, derived

"""  
featureSpaceIndices = np.array([15, 19, 23, 27, 31, 35, 39, 43, 47, 51, 59, 63, 67, 75, 79, 83])
fileName = 'inputs/asc_gyro_r.skl'
allByTime = {}
f = open(fileName, 'r')
headers = f.readline().split()
for line in f:
    splited = line.split() 
    timeStamp = int(splited[0])
    allByTime[timeStamp] = {}
f.close()
allByJoint = {}

for inputIndices in featureSpaceIndices:
    allByJoint[inputIndices] = {} 
time, res = prepareAngularVelocityFromInput(fileName, 63, 2, True, allByTime, allByJoint)
"""









import matplotlib.pyplot as plt
import utils.gaussianFit as gf
import math
import numpy as np
import utils.interpulation as inter
import utils.MovingAverage as ma
import utils.stitching.stitching as loop
import utils.misc.animate as an

MAXIMAL_FRAMES_GAP = 4
def removeLowConfedence(time, angles, weights, plot=False):
    tmpTime = []
    tmpAngles = []  
    for t, a, w in zip(time, angles, weights):
        if(w == 6):
            tmpTime.append(t)
            tmpAngles.append(a)
        else:
            if(plot):
                plt.scatter(t, a, c='yellow', label='Low confedence level')
    return tmpTime, tmpAngles

def clusterByTime(time, frameNumbers, angles, plot=False, minimalCluster=15):
    fracs = []
    lastFrameNum = frameNumbers[0]
    currTime = []
    currAngles = []
    for timeStamp, frameNum, angle in zip(time, frameNumbers, angles):
        if(frameNum - lastFrameNum < MAXIMAL_FRAMES_GAP):
            currTime.append(timeStamp)
            currAngles.append(angle)
        else:
            if(len(currTime) > minimalCluster):
                fracs.append((currTime, currAngles))
            else:
                if(plot):
                    plt.scatter(currTime, currAngles, c='red', label='Weekly clustered samples')  
            currTime = [timeStamp]
            currAngles = [angle]
        lastFrameNum = frameNum
    if(len(currTime) > minimalCluster):
        fracs.append((currTime, currAngles))
    return fracs

def filterOutliers(fracs, plot=False, prob = 0.2):    
    outliersTime = []
    outliersAngles = []
    newFracs = []
    for fracTime, fracAngles in fracs:
        g = gf.fitGassian(fracTime, fracAngles)
        for t, a in zip(fracTime, fracAngles):
            if(g(t,a) < prob):
                outliersTime.append(t)
                outliersAngles.append(a)
        newFracTime = [t for t in fracTime if t not in outliersTime]
        newFracAngles = [a for a in fracAngles if a not in outliersAngles] 
        newFracs.append((newFracTime,newFracAngles))
        if(plot):
            plt.scatter(newFracTime,newFracAngles, c='black')
    if(plot):
        plt.scatter(outliersTime, outliersAngles, c='gray', label='Clusters outliers')
    return newFracs

def cleanFracs(fracs, plot=False, MAwindowSize=8, MAexp=1.4):
    frameSize = math.ceil(np.sqrt(len(fracs)))    
    cleanedParts = []
    originalParts = []
    if(plot):
        pass
        #figOrigin = plt.figure()
        #figCleaned = plt.figure()
    i=1
    for time, values in fracs:
        if(plot):
            pass
            #curr = figOrigin.add_subplot(frameSize, frameSize, i)
            #curr.plot(time,values)
        #length = int((time[-1] - time[0]) / 30)
        time, values  = inter.getUniformSampled(time, values)
        originalParts.append(values)
        cleanesdValues = ma.movingAverage(values, MAwindowSize, MAexp)
        if(plot):
            plt.figure()
            plt.plot(values)
            plt.plot(cleanesdValues)
            plt.show()
            #curr = figCleaned.add_subplot(frameSize, frameSize, i)
            #curr.plot(time,values)
        cleanedParts.append(cleanesdValues)
        i+=1
    return cleanedParts, originalParts

def stitchByDensity(time, angles, plot=False, startGrade=0.93, \
        minimalOverlap=10, maximalOverlap=200, lengthFactor=0, density=10):
    fracs = clusterByTime(time, angles, plot)
    fracs = filterOutliers(fracs, plot)   
    cleanedParts, originalParts = cleanFracs(fracs, plot)
    stitchedParts, partDescriptors = loop.stitch(cleanedParts, startGrade, minimalOverlap, \
                                         maximalOverlap, lengthFactor, density) 
    return cleanedParts, stitchedParts, partDescriptors

def stitchKinect(time, angles, weights=None, plot=False, startGrade=0.93, \
        minimalOverlap=10, maximalOverlap=200, lengthFactor=0, density=10):
    if(plot):
        plt.figure()
        plt.scatter(time, angles, c='yellow', label='Low confedence level')
    if(weights is not None):
        time, angles = removeLowConfedence(time, angles, weights, plot)
    fracs = clusterByTime(time, angles, plot)
    fracs = filterOutliers(fracs, plot)   
    cleanedParts, originalParts = cleanFracs(fracs, plot)
    parts, partDescriptors = loop.stitch(cleanedParts, startGrade, minimalOverlap, \
                                         maximalOverlap, lengthFactor, density)  
    
    if(plot and len(parts) != 0):
        plt.figure()
        plt.plot(parts[-1]) 
        loop.plotDesBypart(originalParts, cleanedParts, partDescriptors)
        loop.plotReconstruction(cleanedParts, partDescriptors[-1])
        plt.show()
        #an.animate( parts[-1])
    return parts[-1], partDescriptors[-1], fracs

    
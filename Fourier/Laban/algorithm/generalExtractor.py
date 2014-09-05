import utils.kinect.angleExtraction as ae
import utils.kinect.jointsMap as jm
import numpy as np
import scipy.stats as st
import utils.interpulation as inter
import utils.MovingAverage as ma
import Laban.analysis.advanceAndRetreate as ar
import Laban.analysis.riseAndSink as rs
import Laban.analysis.expendingVsCondencing as ec
import Laban.analysis.spreadindAndClosing as sp
import Laban.analysis.bindVsFree as bf
import Laban.analysis.lightVsStrong as ls
import Laban.analysis.jump as jump
import Laban.AbstractLabanAnalyzer as aa

def getStats(vec):
    stats = []
    stats.append(np.mean(vec))
    stats.append(np.mean(np.abs(vec)))
    stats.append(np.mean(np.square(vec)))
    stats.append(np.std(vec))
    stats.append(st.skew(vec))
    stats.append(st.kurtosis(vec))
    stats.append(np.max(vec))
    stats.append(np.min(vec))
    stats.append(np.max(np.abs(vec)))
    return stats

def analyzeData(time, data):
    vec = []
    vec+=getStats(data)
    _, un = inter.getUniformSampled(time, data)
    cleaned = ma.movingAverage(un, 20, 1.1)
    vec+=getStats(un)
    velocity = np.diff(cleaned)
    vec+=getStats(velocity)
    acceleration = np.diff(velocity)
    vec+=getStats(acceleration)
    jurk = np.diff(acceleration)
    vec+=getStats(jurk)
    return vec

def getFeatureVec(fileName, joints=None):
    headers = open(fileName, 'r').readline().split()
    #bug in the files
    headers = jm.getFileHeader(headers)
    ver = jm.getVersion(headers)
    vec=[]
    jointsHeaders = headers[2:-4]
    for i,h in enumerate(jointsHeaders):#drop timestamp, frameNum and floor
        if i%4==3:
            continue
        #time, relJoints = ae.getRelative2AncestorPosition(fileName, h, ver)
        if i%4!=0:
            continue 
        if not joints is None and not h in joints:
            continue
        try:#for joints that don't have father and grandfather 
            time, _, angles, _ = ae.getAngleVec(fileName, h, False, ver)
            if len(angles)==0:
                continue
        except Exception, e:#joint without a father
            continue
        vec+=analyzeData(time, angles)
    
    #For directness measurement
    for i in range(len(jointsHeaders)/4):#iterate over joints
        
        #Get the joint's relative position
        time, xs = ae.getRelative2AncestorPosition(fileName, jointsHeaders[4*i], ver)
        vec+=analyzeData(time, xs)
        time, ys = ae.getRelative2AncestorPosition(fileName, jointsHeaders[4*i+1], ver)
        vec+=analyzeData(time, ys)
        time, zs = ae.getRelative2AncestorPosition(fileName, jointsHeaders[4*i+2], ver)
        vec+=analyzeData(time, zs)
        
        #Get its change
        xs = np.diff(xs)
        ys = np.diff(ys)
        zs = np.diff(zs)
        
        #Make movement vectors
        movements = zip(xs, ys, zs)
        dircetness = []
        for i in range(len(movements)-1):
            first = ae.getUnitVec(movements[i])
            second = ae.getUnitVec(movements[i+1])
            dircetness.append(np.dot(first, second))
        vec+=analyzeData(time[1:-1], dircetness)
        
    extractor = aa.getExtractor(fileName)
    #AdvanceAndRetreate
    advancements = ar.AdvanceAndRetreate(extractor).extract(fileName)
    vec+=getStats(advancements)
    
    #RiseAndSink
    advancements = rs.RiseAndSink(extractor).extract(fileName)
    vec+=getStats(advancements)
    
    #ExpendingCondencing
    advancements = ec.ExpendingCondencing(extractor).extract(fileName)
    vec+=getStats(advancements)
    
    #SpreadindAndClosing
    advancements = sp.SpreadindAndClosing(extractor).extract(fileName)
    try:
        vec+=getStats(advancements)
    except:
        advancements = sp.SpreadindAndClosing(extractor).extract(fileName)
     #   pass
    
    #FreeAndBind
    extractor = aa.getExtractor(fileName)
    advancements = bf.FreeAndBind(extractor).extract(fileName)
    vec+=getStats(advancements)
    
    #LightAndStrong
    extractor = aa.getExtractor(fileName)
    advancements = ls.LightAndStrong(extractor).extract(fileName)
    vec+=getStats(advancements)
    
    #Jump
    extractor = aa.getExtractor(fileName)
    advancements = jump.Jump(extractor).extract(fileName)
    try:
        vec+=getStats(advancements)
    except:
        pass
    
    #Sudden
    #Is the skew of the velocity of the joints.
    
    
    return vec











import utils.kinect.angleExtraction as ae
import utils.kinect.jointsMap as jm
import numpy as np
import scipy.stats as st
import utils.interpulation as inter
import utils.MovingAverage as ma
import Laban.analysis.advanceAndRetreate as ar
import Laban.analysis.riseAndSink as rs
import Laban.AbstractLabanAnalyzer as aa
def getStats(vec):
    stats = []
    stats.append(np.mean(vec))
    stats.append(np.mean(np.abs(vec)))
    stats.append(np.mean(np.square(vec)))
    stats.append(np.std(vec))
    stats.append(st.kurtosis(vec))
    stats.append(np.max(vec))
    stats.append(np.min(vec))
    return stats

def getFeatureVec(fileName, joints=None):
    headers = open(fileName, 'r').readline().split()
    #bug in the files
    headers = jm.getFileHeader(headers)
    ver = jm.getVersion(headers)
    vec=[]
    
    for i,h in enumerate(headers[2:-4]):#drop timestamp, frameNum and floor
        if i%4!=0:
            continue 
        if not joints is None and not h in joints:
            continue
        try:
            time, _, angles, _ = ae.getAngleVec(fileName, h, False, ver)
            if len(angles)==0:
                continue
        except Exception, e:#joint without a father
            continue
        vec+=getStats(angles)
        _, un = inter.getUniformSampled(time, angles)
        cleaned = ma.movingAverage(un, 20, 1.1)
        vec+=getStats(un)
        velocity = np.diff(cleaned)
        vec+=getStats(velocity)
        acceleration = np.diff(velocity)
        vec+=getStats(acceleration)
        jurk = np.diff(acceleration)
        vec+=getStats(jurk)
    extractor = aa.getExtractor(fileName)
    advancements = ar.AdvanceAndRetreate(extractor).extract(fileName)
    vec+=getStats(advancements)
    #ups = 
    return vec











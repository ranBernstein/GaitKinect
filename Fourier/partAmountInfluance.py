import numpy as np
from utils.amcParser import getAMCInput
from utils.timinigOneStride import getSwingsAndStances
from multiprocessing import Pool
from utils.stitching import EPSILON_FACTOR, GAP_FACTOR, MEAN_COEFF,OVERLAP_FACTOR,STD_COEFF, plotParts
import utils.stitching as st
import utils.stitchingLoop as loop
import matplotlib.pyplot as plt
import math
from scipy.stats import variation
import utils.MovingAverage as ma

numOfFeatures = 100
subjects = [8, 16, 35 ,39]
joint = 'rtibia'
index =0
partsAmount=9
noiseStdFactor = 80.0
testAmount = 50
stitchesNum = 24
scores = {}

def getCV(vec):
    #mean =  np.mean(vec)
    #return [np.abs(math.sqrt(np.abs(x**2-mean**2))/mean) for x in vec]
    return variation(vec)

def evalParams(partsAmount):
    noiseStdFactor = 0.02       
    stances = {}
    swings = {}
    for subject in subjects:
        for index in xrange(8):
            try:
                input = getAMCInput(joint, subject, index)
            except:
                continue
            amplitude = np.max(input) - np.min(input)
            var = (amplitude*noiseStdFactor)**2
            for stitch in xrange(stitchesNum):
                try:
                    noisy_parts = st.createParts(input, False, partsAmount, var)
                except:
                    continue
                parts = ma.partsmovingAverage(noisy_parts)
                stitched_parts, des = loop.stitch(parts)
                if(len(stitched_parts) == len(parts)):
                    continue
                stitched = stitched_parts[-1]
                input = stitched
                tmpSwings, tmpStances = getSwingsAndStances(input)
                key = (stitch, subject) 
                for stanceLen, swingLen in zip(tmpStances, tmpSwings):
                    if(stanceLen > 55):
                        stances[key] = stances.get(key, []) + [stanceLen]
                    if(swingLen > 35):
                        swings[key] = swings.get(key, []) + [swingLen]
    stancesCV = []
    swingsCV = []
    strideCV = []
    strideLengths = {}
    stancesLengths = {}
    swingsLengths = {}
    for stitch in xrange(stitchesNum):
        for subject in subjects:
            key = (stitch, subject)
            stance = None
            if not(key in stances and key in swings):
                continue
            stance = stances[key]
            cv = getCV(stance)
            if not math.isnan(cv) and 0 < cv :
                stancesCV.append(cv)
            stancesLengths[subject] = stancesLengths.get(subject, []) + stance
            
            swing = swings[key]
            cv = getCV(swing)
            if not math.isnan(cv) and 0 < cv :
                swingsCV.append(cv)
            swingsLengths[subject] = swingsLengths.get(subject, []) + swing
            
            strideLength = [x+y for x,y in zip(stance, swing)]
            cv = getCV(strideLength)
            if not math.isnan(cv) and 0 < cv :
                strideCV.append(cv)
            strideLengths[subject] = strideLengths.get(subject, []) + strideLength
    
    stancesLengths = [stancesLengths[subject] for subject in stancesLengths]
    swingsLengths = [swingsLengths[subject] for subject in swingsLengths]
    strideLengths = [strideLengths[subject] for subject in strideLengths]
    strideReference = [115.61538461538461, 113.66666666666667, 116.11111111111111, 126.375]
    strideMeans = [np.mean(seq) for seq in strideLengths]
    finalGrade = np.mean([np.abs(y-x)/x for x,y in zip(strideReference, strideMeans)])   
    stanceCVmean = np.mean(stancesCV)
    swingCVmean = np.mean(swingsCV)
    strideCVsMean = np.mean(strideCV)
    titles = ['Subject: ' + str(x) for x in subjects]
    #plotParts(stancesLengths, 'Stance number', 'Stance time(in frames)', titles)
    #plotParts(swingsLengths, 'Swing number', 'Swing time(in frames)', titles)
    #plotParts(strideLengths, 'Stride number', 'Stride time(in frames)', titles)
    print 'partsAmount', partsAmount
    print stanceCVmean, [np.mean(seq) for seq in stancesLengths]
    print  swingCVmean, [np.mean(seq) for seq in swingsLengths]
    print strideCVsMean, strideMeans
    return finalGrade

if __name__ == '__main__':  
    partsAmounts = xrange(2,43)#[2, 5, 8, 11, 13, 15, 17, 19, 21, 23]
    p = Pool(7)
    results = {}
    for partsAmount in partsAmounts:
        results[partsAmount] = p.apply_async(evalParams, [partsAmount]) 
    p.close()
    p.join()
    grades = []
    for partsAmount in partsAmounts:
        grades.append(results[partsAmount].get())
    plt.plot(partsAmounts, grades)
    plt.ylim([0,0.2])
    plt.show()


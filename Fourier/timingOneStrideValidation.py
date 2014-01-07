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

numOfFeatures = 100
subjects = [8, 16, 35 ,39]
joint = 'rtibia'
index =0
partsAmount=20
noiseVariance = 0.01
testAmount = 50
stitchesNum = 2
scores = {}

def getCV(vec):
    #mean =  np.mean(vec)
    #return [np.abs(math.sqrt(np.abs(x**2-mean**2))/mean) for x in vec]
    return variation(vec)

def evalParams(m1=MEAN_COEFF, m2=STD_COEFF,  epsilon=EPSILON_FACTOR,gap=GAP_FACTOR, overlap=OVERLAP_FACTOR):       
    sum = 0
    stances = {}
    swings = {}
    for stitch in xrange(stitchesNum):
        for subject in subjects:
            for index in xrange(8):
                try:
                    input = getAMCInput(joint, subject, index)
                except:
                    continue
                parts = st.createParts(input, True, partsAmount, noiseVariance)
                #stitched = st.stitch(parts, m1, m2, epsilon,gap, overlap)
                stitched = loop.stitch(parts)[-1]
                input = stitched
                tmpSwings, tmpStances = getSwingsAndStances(input)
                key = (stitch, subject) 
                stances[key] = stances.get(key, []) + tmpStances
                swings[key] = swings.get(key, []) + tmpSwings
    stancesCV = []
    swingsCV = []
    strideCV = []
    strideLengths = {}
    stancesLengths = {}
    swingsLengths = {}
    for stitch in xrange(stitchesNum):
        for subject in subjects:
            key = (stitch, subject)
            
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
    
    stancesLengths = [stancesLengths[subject] for subject in subjects]
    swingsLengths = [swingsLengths[subject] for subject in subjects]
    strideLengths = [strideLengths[subject] for subject in subjects]
        
    stanceCVmean = np.mean(stancesCV)
    swingCVmean = np.mean(swingsCV)
    strideCVsMean = np.mean(strideCV)
    titles = ['Subject: ' + str(x) for x in subjects]
    plotParts(stancesLengths, 'Stance number', 'Stance time(in frames)', titles)
    plotParts(swingsLengths, 'Swing number', 'Swing time(in frames)', titles)
    plotParts(strideLengths, 'Stride number', 'Stride time(in frames)', titles)
    print 'len(stances)', len(stances)
    print stanceCVmean, [np.mean(seq) for seq in stancesLengths]
    print  swingCVmean, [np.mean(seq) for seq in swingsLengths]
    print strideCVsMean, [np.mean(seq) for seq in strideLengths]

evalParams(0.065, 0.05, 0.08)
plt.show()
"""
if __name__ == '__main__':  
    results = {}  
    scale = np.linspace(0.001, 0.3, 5) 
    m1=0.13
    m2=0.09
    epsilon = 0.15
    p = Pool(3)
    for measured in scale:
        #for m2 in momentss:
        #results[measured] = evalParams(m1, m2, epsilon, measured)
        results[measured] = p.apply_async(evalParams, [m1, m2,epsilon, measured]) 
    p.close()
    p.join()
    for measured in scale:
        res = results[measured].get()
        print '/n', measured, res
    
    print 'scores:'
    print scores
"""

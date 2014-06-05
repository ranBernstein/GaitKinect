from utils.vicon.amcParser import getAMCInput
from utils.periodAnalysisUtils import alignByMax
import matplotlib.pyplot as plt
import math
import numpy as np
import utils.interpulation as inter
from sklearn import datasets
from sklearn.neighbors import KNeighborsClassifier
import random
import copy
import utils.stitching.stitching as st
import utils.stitching.stitching.partitionizing as pr
import utils.periodAnalysisUtils as ut
from utils.misc import crossValidate.crossValidate
from multiprocessing import Pool
from utils.stitching import EPSILON_FACTOR, GAP_FACTOR, MEAN_COEFF,OVERLAP_FACTOR,STD_COEFF
from sklearn import svm

numOfFeatures = 100
subjects = [8, 16, 35 ,39]
joint = 'rtibia'
index =0
partsAmount=9
testAmount = 50
stitchesNum = 40
scores = {}

def evalParams(m1=MEAN_COEFF, m2=STD_COEFF,  epsilon=EPSILON_FACTOR,gap=GAP_FACTOR, overlap=OVERLAP_FACTOR):       
    sum = 0
    for stitch in xrange(stitchesNum):
        data = []
        tags = []
        for subject in subjects:
            for index in xrange(8):
                try:
                    input = getAMCInput(joint, subject, index)
                except:
                    continue
                parts = st.createParts(input, partsAmount)
                stitched = st.stitch(parts, m1, m2, epsilon,gap, overlap)
                #plt.figure()
                #plt.plot(stitched)
                periods = pr.breakToPeriods(stitched)
                periods = ut.alignByMaxMany(periods)
                periods = inter.getUniformSampledVecs(periods, 100)
                data = data + periods
                tags = tags + [subject]*len(periods)
                #st.plotParts(periods)
        
        cl = KNeighborsClassifier()
        cl.n_neighbors = 5
        cl.weights = 'distance' 
        testSize = 1
        score = crossValidate(cl, data, tags, testSize, testAmount)
        #print str(m2)+' '+ str(score)
        sum+=score
    score = float(sum)/stitchesNum
    scores[m1, m2] = score
    return score
    #print '/nm2: ', m2, ' m1: ', m1,' score: ', score

if __name__ == '__main__':  
    results = {}  
    scale = np.linspace(0.01, 0.12, 3) 
    m1=0.13
    m2=0.09
    epsilon = 0.15
    gap = 0.15
    overlap = 0.1
    p = Pool(3)
    for measured in scale:
        results[measured] = p.apply_async(evalParams, [m1, m2,epsilon, gap, overlap]) 
    p.close()
    p.join()
    print 'ovelap'
    for measured in scale:
        res = results[measured].get()
        print '/n', measured, res
    
    print 'scores:'
    print scores


import matplotlib.pyplot as plt
import numpy as np
from Fourier import getFourier
from Cleaner import *
from amcParser import *

def plotPeriodsTogether(file, joint):
    periods= plotJointCenteredPeriodicaly(file, joint)
    for period in periods:
        plt.plot(range(len(period)), period)
    plt.show()

def plotEveryPeriodWithFourier(file, joint):
    periods= plotJointCenteredPeriodicaly(file, joint)
    for period in periods:
        series, coeffs, normalizedCoeffs = getFourier(period, coeffNum)
        plt.plot(range(len(period)), period)
        plt.plot(range(len(period)), series)        
        plt.show()
        plt.scatter(range(len(normalizedCoeffs)), normalizedCoeffs)
        plt.ylim((0,1))
        plt.show()

def plotEveryPeriodWithFourierWithoutBias(file, joint):   
    periods= plotJointCenteredPeriodicaly(file, joint)
    periods=cleanPeriodsBias(periods)
    maxLength = getMaxLenOfLists(periods) 
    for period in periods:
        series, coeffs, normalizedCoeffs = getFourier(period, coeffNum)
        plt.plot(range(len(period)), period)
        plt.plot(range(len(period)), series)        
        plt.show()
        plt.scatter(range(len(normalizedCoeffs)), normalizedCoeffs)
        plt.ylim((0,1))
        plt.xlim((0,coeffNum))
        plt.show()

def plotCoeffsCompare(file, joint, periods):
    maxLength = getMaxLenOfLists(periods);
    for period in periods:
        i= np.random.random(10)
        series, coeffs, normalizedCoeffs = getFourier(period, maxLength, coeffNum)
        plt.scatter(range(len(coeffs)), coeffs, c=i, s=500)       
    plt.show()
    
def plotNormalizedCoeffsCompare(file, joint, periods):
    maxLength = getMaxLenOfLists(periods);
    for period in periods:
        i= np.random.random(10)
        series, coeffs, normalizedCoeffs = getFourier(period, coeffNum)
        plt.scatter(range(len(normalizedCoeffs)), normalizedCoeffs, c=i, s=500)       
    plt.show()

def accumlateCoeffsCompare(file, joint, periods):
    maxLength = getMaxLenOfLists(periods);
    accumCoeffs=[]
    for period in periods:
        i= np.random.random(10)
        accumulatedCoeffs = []
        series, coeffs, normalizedCoeffs = getFourier(period, coeffNum)
        accumCoeffs.append(normalizedCoeffs)
    meanList = getMeanList(accumCoeffs)
    return accumulateList(meanList)
def perJointAnalysis(file, joint):
    periods_x = plotJointCenteredPeriodicaly(file, joint)
    periods_y = plotJointCenteredPeriodicaly(file, joint)
    periods_z = plotJointCenteredPeriodicaly(file, joint)
    sumCoeffs = []   
    coeffs_x = accumlateCoeffsCompare(file, joint, periods_x, False)
    coeffs_y = accumlateCoeffsCompare(file, joint, periods_y, False)
    coeffs_z = accumlateCoeffsCompare(file, joint, periods_z, False)
    for i in range(coeffNum):
        tmp = (coeffs_x[i]**2 + coeffs_y[i]**2 + coeffs_z[i]**2)**0.5
        sumCoeffs.append(tmp)
    plt.scatter(range(len(sumCoeffs)), sumCoeffs)
    plt.show()

def compareAmcKinect(file, joint, coeffNum, periods):
    series, coeffs, normalizedCoeffs = getFourier(getAMCperiod(), coeffNum)
    vicon = accumulateList(normalizedCoeffs)
    plt.scatter(range(len(vicon)), vicon)
    
    kinect  = accumlateCoeffsCompare(file, joint, periods)
    plt.scatter(range(len(kinect)), kinect)
    plt.legend('vk')
    plt.show()   

def PlotWholeAMC():
    period  = getAMCperiod(False, 0, 0)
    period = cleanSeriesBias(period)
    plt.plot(range(len(period)),period,color='blue')
    plt.show()

def plotAMCCompare(coeffNum):
    period =  getAMCperiod(True, 60, 176)
    period = cleanSeriesBias(period)
    series, coeffs, normalizedCoeffs = getFourier(period, coeffNum)
    plt.scatter(range(len(normalizedCoeffs)),normalizedCoeffs,color='blue')
    
    period =  getAMCperiod(True, 177, 298)
    period = cleanSeriesBias(period)
    series, coeffs, normalizedCoeffs = getFourier(period, coeffNum)
    plt.scatter(range(len(normalizedCoeffs)),normalizedCoeffs,color='red')
    
    plt.show()        
file = 'inputs/assaf_45.skl'
joint = Joints.WristRight_Y
coeffNum = 20
periods= plotJointCenteredPeriodicaly(file, joint)
nonBiasPeriods=cleanPeriodsBias(periods)

plotJointCentered(file, joint)
#plotNormalizedCoeffsCompare(file, joint, nonBiasPeriods)
#plotPeriodsTogether(file, joint)

#accumlateCoeffsCompare(file, joint, periods, False)
#perJointAnalysis(file, joint)






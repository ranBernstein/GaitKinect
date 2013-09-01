import numpy as np
import matplotlib.pyplot as plt
from itertools import *

def calcCoeffN(n, y, time, period):
    inx = -1j*2*n*np.pi*time/period
    c = y*np.exp(inx)
    return c.sum()/c.size

def getCoeffs(func, time, period, coeffNum):
    coeffRaw = [];
    sum=0;
    for i in range(coeffNum):
        coeffRaw.append(abs(calcCoeffN(i, func, time, period)));
    return coeffRaw

def getNormalizedCoeffs(func, time, period, coeffNum): 
    coeffRaw = [];
    sum=0;
    for i in range(coeffNum):
        sum+=abs(calcCoeffN(i, func, time, period));   
    coeffNormalized = [];
    for i in range(coeffNum):
        coeffNormalized.insert(i, abs(calcCoeffN(i, func, time, period))/sum);
    return coeffNormalized
    

def getfourierDecomposition(func, time, period, coeffNum):
    y2 = np.array([fourierValue(t,coeffNum, func, time, period).real for t in time])
    return y2


def fourierValue(x, Nh, y, time, period):
    rng = np.arange(.5, Nh+.5)
    fourierValue = np.array([2*calcCoeffN(i, y, time, period)*np.exp(1j*2*i*np.pi*x/period) for i in rng])
    return fourierValue.sum()


def getFourier(func, coeffNum):
    a = 1.0
    b = -1.0
    time = np.linspace( a, b, len(func))
    period = 2.
    values = getfourierDecomposition(func, time, period, coeffNum)
    rawCoeffs = getCoeffs(func, time, period, coeffNum)
    normalizedCoeffs = getNormalizedCoeffs(func, time, period, coeffNum)
    return [values, rawCoeffs, normalizedCoeffs]

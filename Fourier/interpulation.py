import numpy as np
import matplotlib.pyplot as plt
import angleExtraction
from scipy.interpolate import interp1d
import scipy 

def scaleVec(input, scaleFactor):
    x = np.linspace(0, len(input),  len(input))
    f = interp1d(x, input, kind='cubic')
    scaled_x =  np.linspace(0, len(input), int(len(input)*scaleFactor))
    return f(scaled_x)

def getScaledVectors(input):
    scaleFactors = [ 0.85, 0.9, 0.93, 0.95, 0.97, 0.985, 1, 1.015, 1.03]#, 1.06, 1.1, 1.15, 1.2]
    vectors = []
    for scaleFactor in scaleFactors:
        vectors.append(scaleVec(input, scaleFactor))
    return vectors

def getUniformSampled(values, time, length=None):
    f = interp1d(time, values, kind='cubic')
    if length==None:
        length  = len(values)
    x = np.linspace(time[0], time[-1],  length)
    return f(x), x
    
"""
x = xrange(50)
y = np.sin(x)
plt.plot(xrange(len(vec)), vec)
plt.show()
"""
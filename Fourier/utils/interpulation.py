import numpy as np
from scipy.interpolate import interp1d

def scaleVec(input, scaleFactor):
    x = np.linspace(0, len(input),  len(input))
    f = interp1d(x, input, kind='cubic')
    scaled_x =  np.linspace(0, len(input), int(len(input)*scaleFactor))
    return f(scaled_x)

def getScaledVectors(input):
    scaleFactors = [1]#[ 0.85, 0.9, 0.93, 0.95, 0.97, 0.985, 1, 1.015, 1.03]#, 1.06, 1.1, 1.15, 1.2]
    vectors = []
    for scaleFactor in scaleFactors:
        vectors.append(scaleVec(input, scaleFactor))
    return vectors

def getUniformSampled(time, values, length=None):
    f = interp1d(time, values, kind='linear')
    if length==None:
        length  = len(values)
    x = np.linspace(time[0], time[-1],  length)
    retval = x, f(x)
    #except Exception, e:
    return retval

def getUniformSampledVecs(vecs, length=None):
    y_s = []
    for vec in vecs:
        x, y= getUniformSampled(xrange(len(vec)), vec, length)
        y_s.append(y)
    return y_s
    
"""
x = xrange(50)
y = np.sin(x)
plt.plot(xrange(len(vec)), vec)
plt.show()
"""
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
    scaleFactors = [0.80, 0.85, 0.9, 0.95, 1, 1.05, 1.1, 1.15, 1.2]
    vectors = []
    for scaleFactor in scaleFactors:
        vectors.append(scaleVec(input, scaleFactor))
    return vectors
"""
x = xrange(50)
y = np.sin(x)
for vec in getScaledVectors(y):
    plt.plot(xrange(len(vec)), vec)
plt.show()
"""
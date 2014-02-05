import numpy as np
from scipy import optimize 

def gaussian(height, center_x, center_y, width_x, width_y):
    """Returns a gaussian function with the given parameters"""
    width_x = float(width_x)
    width_y = float(width_y)
    return lambda x,y: height*np.exp(
                -(((center_x-x)/width_x)**2+((center_y-y)/width_y)**2)/2)

def moments(xs, ys):
    x = np.mean(xs)
    y = np.mean(ys)
    width_x = np.std(xs)
    width_y = np.std(ys)
    height = 1
    return (height, x, y, width_x, width_y)

def fitGassian(xs, ys):
    return gaussian(*moments(xs, ys))
"""  
xs = [1,3,5]
ys = [1,6,1]

print g(0,0)
print g(3,3)
"""
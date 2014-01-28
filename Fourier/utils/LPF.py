import scipy.signal as sig
import numpy as np
import matplotlib.pyplot as plt
import interpulation
import copy
from operator import add
def clean(y_p, N=10, time=None):
    y = map(add, [-y_p[0]]*len(y_p), y_p)
    clean_time = None
    if(time is not None):
        y, clean_time = interpulation.getUniformSampled(y, time)
    Fs=1600
    # provide them to firwin
    h=sig.firwin( numtaps=N, cutoff=40, nyq=Fs/2)
    clean=sig.lfilter( h, 1.0, y) # 'x' is the time-series data you are filtering
    clean = map(add, [ y_p[0]]*len(clean), clean)
    return clean#, clean_time
"""
x = np.linspace(0, 10,  50) 
y = np.sin(x)   
z = clean(y)
plt.plot(x,y, color = 'blue')
plt.plot(x,z, color = 'green')
plt.show()
"""
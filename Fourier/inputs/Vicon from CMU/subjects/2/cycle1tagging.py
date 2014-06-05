import matplotlib.pyplot as plt
import numpy as np
from Fourier import getFourier
from Cleaner import *



def getAMCperiod(period=False, start=0, end=0):
    file = 'AMCs/subjects/1/1.amc'
    f = open(file, 'r')
    input = []
    for line in f:
        if 'ltibia' in line:
            input.append(float(line.split()[1]))
    if(period):
        input = input[start:end]  # getPeriod
    return input

input = getAMCperiod()
fig = plt.figure()
ax = fig.add_subplot(111)
ax.plot(range(len(input)), input)
ax.set_xlabel('Time (in frames)')
ax.set_ylabel('Left knee angle')
ax.annotate('Terminal stance', xy=(67, 9.3), xytext=(67, 3), arrowprops=dict(facecolor='black', shrink=0.05),)
ax.annotate('Initial swing', xy=(103, 73), xytext=(103, 75), arrowprops=dict(facecolor='black', shrink=0.05),)
ax.annotate('Terminal swing', xy=(134, 23), xytext=(110, 15), arrowprops=dict(facecolor='black', shrink=0.05),)
ax.annotate('Loading response', xy=(19, 37), xytext=(19, 48), arrowprops=dict(facecolor='black', shrink=0.05),)
plt.show()
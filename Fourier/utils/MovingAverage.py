import numpy as np
import matplotlib.pyplot as plt
import utils as pu

def partsmovingAverage(parts, window_size=8, factor=1.3):
    cleanParts = []
    for part in parts:
        clean = movingAverage(part, window_size, factor)
        cleanParts.append(clean)
    return cleanParts



def movingAverage(interval, window_size, factor):
    interval = pu.toList(interval)
    if(window_size %2 == 0):
        window_size += 1
    
    window = np.ones(int(window_size))
    half = int(window_size/2)
    center = half + 1
    for i in xrange(1, center):
        window[half + i] = window[half + i -1]/float(factor)
        window[half - i] = window[half - i + 1]/float(factor) 
    s = np.sum(window)
    window = [x/s for x in window]
    head = [np.mean(interval[:window_size])]*window_size
    tail = [np.mean(interval[-window_size:])]*window_size
    conv = np.convolve(head + interval + tail, window, 'same')
    retVal = conv[window_size:-window_size] 
    return pu.toList(retVal)

def mse(A, B):
    return ((np.array(A) - np.array(B)) ** 2).mean(axis=0)
def me(A, B):
    return np.mean([np.abs(x-y) for x, y in zip(A,B)])
"""
file = '../AMCs/598.amc'
joint = 'rtibia'
list = getAMCperiod(joint, file)
stride = list[112:251] 
list = ut.alignByMax(stride)
amplitude = np.max(list) - np.min(list)
windowSizes = xrange(1, len(list)/4)
def checkFactor(factor):
    mses = []
    for window_size in windowSizes:
        sums = []
        for i in xrange(100):
            noise = map(add, np.random.normal(0,amplitude/8,len(list)), list)
            ma = movingAverage(noise, window_size, factor)
            sums.append(me(list, ma))
        mses.append(np.mean(sums))
    plt.plot(windowSizes, mses, label='factor: ' + str(factor))
factors = [1, 1.01, 1.05, 1.1, 1.2, 1.3, 1.8]
for factor in factors:
    checkFactor(factor)
#plt.plot(list, c='b')
#plt.plot(ma, c='g')
#plt.plot(noise, c='r')
#plt.plot(LPFed, c='black')
plt.xlabel('window size')
plt.ylabel('me')
plt.title('Mean error as function of window size of differnt windows')
plt.legend().draggable()
plt.show()
"""
import numpy as np

def clusterByPercemtile(vec, windowSize, percentile):
    windowSize = min(windowSize, len(vec))
    newVec = []
    upGlobal = np.percentile(vec, percentile)-5
    downGlobal = np.percentile(vec, 100-percentile)+5
    for i in range(len(vec)):
        if i < windowSize/2:
            left = 0
            right = windowSize - i
        else:
            if len(vec) - i < windowSize/2:
                right = len(vec)-1
                left = i - (windowSize - (len(vec) - i))
            else:
                right = i+windowSize/2
                left = i - windowSize/2
        
        window = vec[left:right]
        up = np.percentile(window, percentile)
        down = np.percentile(window, 100-percentile)
        if vec[i] > up and vec[i] > upGlobal:
            newVec.append(1)
        else:
            if vec[i] < down and vec[i]<downGlobal:
                newVec.append(-1)
            else:
                newVec.append(0)
    return newVec
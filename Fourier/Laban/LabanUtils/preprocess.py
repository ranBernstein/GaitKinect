import numpy as np

def chopHeadAndTail(positionVec, chopingFactor):
    velocity = np.diff(positionVec)
    velocityMagnitude = np.abs(velocity)
    m = np.mean(velocityMagnitude)
    threshold = m*chopingFactor
    
    for i,v in enumerate(velocityMagnitude):
        if v > threshold:
            firstIndex = i
            break
    
    for i,v in enumerate(reversed(velocityMagnitude)):
        if v > threshold:
            lastIndex = len(velocityMagnitude) - i
            break
    
    return firstIndex, lastIndex
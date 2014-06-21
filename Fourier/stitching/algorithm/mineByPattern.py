import numpy as np
from operator import sub
import utils.utils as pe
import networkx as nx
import MovingAverage as ma
import matplotlib.pyplot as plt
import itertools
def getDistanceBetweenFracs(f1, o1, f2, o2):
    if(o1 > o2):
        f1, o1, f2, o2 = f2, o2, f1, o1
    if(o1 + len(f1)  < o2 + 2):
        return np.inf
    startPoint1 = max(o1, o2) - o1
    startPoint2 = max(o1, o2) - o2
    endPoint1 = min(o1+len(f1), o2 + len(f2)) - o1
    endPoint2 = min(o1+len(f1), o2 + len(f2)) - o2
    try:
        diff = np.abs(map(sub, f1[startPoint1:endPoint1], f2[startPoint2:endPoint2]))
    except Exception, e:
        pass
    return np.mean(diff)

def mergeVecs(first, firstOffset, firstList, second, secondOffset, secondList):
    first = pe.toList(first)
    second = pe.toList(second) 
    if(secondOffset < firstOffset):
        first, firstOffset, second, secondOffset = (second, secondOffset, first, firstOffset)
    if(firstOffset + len(first) < secondOffset + 2):
        return None    
    head = first[:(secondOffset - firstOffset)]
    overlapStart = secondOffset
    overlapEnd= min(firstOffset + len(first), secondOffset + len(second))
    def average(e1, e2):
        return (e1+e2)/2.0
    common = map(average, first[(overlapStart-firstOffset):(overlapEnd-firstOffset)],
                  second[(overlapStart-secondOffset):(overlapEnd-secondOffset)])
    tail = second[len(common):] if  secondOffset + len(second) > firstOffset + len(first) \
        else first[len(common):]
    return head + common + tail, firstOffset, firstList+secondList

def matchFracsByPositionInCycle(minedParts, numberOfStrides):
    changeWasMade = True
    while(changeWasMade):
        changeWasMade = False
        for i in xrange(len(minedParts)):
            if changeWasMade:
                break
            for j in xrange(i):
                dis = getDistanceBetweenFracs(minedParts[i][0], minedParts[i][1], 
                                              minedParts[j][0], minedParts[j][1])
                if(dis > 3):
                    continue
                #print dis 
                retVal = mergeVecs(minedParts[i][0], minedParts[i][1],  
                    minedParts[i][2], minedParts[j][0], minedParts[j][1], minedParts[j][2])
                if(retVal is None):
                    continue
                merged, off, newList = retVal
                del minedParts[i]
                del minedParts[j]
                minedParts.append((merged, off, newList))
                changeWasMade = True
                break
    return minedParts

def createFlippedUpattern(vec, length, repeatitionAmount=1):
    up1 = np.linspace(0, 10, length/4).tolist()
    up2 = np.linspace(10, 40, length/4).tolist()
    down1 = np.linspace(40, 10, length/4).tolist()
    down2 = np.linspace(10, 0, length/4).tolist()
    pattern = up1 + up2 + down1 + down2
    smoothedPattern = ma.movingAverage(pattern, length/5, 1.3)
    pattern = smoothedPattern
    pattern = [x-np.mean(pattern) for x in pattern]
    fac = np.sqrt(np.var(vec)/np.var(pattern))
    m1 = np.mean(vec)
    pattern = [x*fac + m1 for x in pattern]
    #retVal = list(itertools.repeat(pattern, repeatitionAmount))
    retVal = pattern*repeatitionAmount
    return retVal



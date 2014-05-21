import numpy as np
from operator import sub
import utils.periodAnalysisUtils as pe

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

def matchFracsByPositionInCycle(minedParts):
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
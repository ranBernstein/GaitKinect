import copy
import math
import numpy as np

def magnitude(v):
    return math.sqrt(sum(v[i]*v[i] for i in range(len(v))))

def normalize(v):
    vmag = magnitude(v)
    if(vmag == 0):
        return v
    return [ v[i]/vmag  for i in range(len(v)) ]

def correlate(vec1, vec2, minimalOverlap):
    if(len(vec1) != len(vec2)):
        raise 'correlate: vectors not from the same lengths'
    vec1 = normalize(vec1)
    vec2 = normalize(vec2)
    c = np.correlate(vec1, vec2)[0]
    return  (c + len(vec1))/(c + len(vec1) + minimalOverlap)

def euclidean(vec1, vec2, minimalOverlap=1, lenFac=1.0):
    if(len(vec1) != len(vec2)):
        raise 'correlate: vectors not from the same lengths'
    mean = np.mean([np.abs(v1-v2) for v1, v2 in zip(vec1, vec2)])
    if mean == 0:
        return 1
    m= 1.0/mean
    return 1 if m==0 else (m/(m+0.01) + lenFac*float(len(vec1))/(len(vec1)+1))/(1+lenFac) 

def slidingOver(vec1, vec2, overLapGrader, minimalOverlap, averageGrade, lenFac):
    big, small = (vec1, vec2) if len(vec1) > len(vec2) else (vec2, vec1)
    bestGrade = -1
    bigStart = None
    smallStart = None
    bestOverlap  = None
    for i in reversed(xrange(minimalOverlap, len(small))):
        grade =  overLapGrader(big[:i], small[-i:], minimalOverlap)
        if(grade > bestGrade):
            bestGrade = grade
            bigStart = 0
            smallStart = len(small) - i
            bestOverlap = i
        
    for i in xrange(len(big)-minimalOverlap):
        overlapSize = min(len(small), len(big) - i)
        grade =  overLapGrader(small[:overlapSize], big[i:i+overlapSize], minimalOverlap, lenFac)
        if(grade > bestGrade):
            bestGrade = grade
            bigStart = i
            smallStart = 0
            bestOverlap = overlapSize
    print bestGrade
    if(bestGrade < 0.99*averageGrade):
        return [], None
    mergedVec = big[:bigStart] + \
    small[:smallStart] + \
    [(x+y)/2 for x, y in zip(big[bigStart:bigStart+bestOverlap], small[smallStart:smallStart+bestOverlap])] + \
    big[bigStart+ bestOverlap:] + \
    small[smallStart + bestOverlap:]
    return mergedVec, bestGrade

def stitch(parts, matchFrame=slidingOver, overLapGrader=euclidean, minimalOverlap=5, lenFac=0.2):
    parts = copy.copy(parts)
    changeWasMade = True
    grades = []
    while(changeWasMade):
        changeWasMade = False
        for i in xrange(len(parts)):
            if changeWasMade:
                break
            for j in xrange(i):
                average = 0 if len(grades) == 0 else  np.mean(grades)
                stitched, grade = matchFrame(parts[i], parts[j], overLapGrader, minimalOverlap, average, lenFac)
                if grade is not None:
                    grades.append(grade)
                if(len(stitched) == 0):
                    continue
                del parts[max(i,j)]
                del parts[min(i,j)]
                parts.append(stitched)
                changeWasMade = True
                break
    return parts
"""
print alignBySmall([0, 0, 1,2,3,0,0], [1,2,3], euclidean)
"""
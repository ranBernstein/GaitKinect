import copy
import math
import numpy as np
import matplotlib.pyplot as plt
#import matplotlib.animation as animation
#import utils.misc.animate as an
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

def euclidean(vec1, vec2, lenFac):
    if(len(vec1) != len(vec2)):
        raise 'correlate: vectors not from the same lengths'
    mean = np.mean([np.abs(v1-v2) for v1, v2 in zip(vec1, vec2)])
    if mean == 0:
        return 1
    m= 1.0/mean
    return 1 if m==0 else (m/(m+0.01) + lenFac*float(len(vec1))/(len(vec1)+1))/(1+lenFac) 

def slidingOver(vec1, vec1Des, vec2, vec2Des, overLapGrader, minimalOverlap, maximalOverlap, \
                averageGrade, lenFac, density, parts):
    big, small = (vec1, vec2) if len(vec1) > len(vec2) else (vec2, vec1)
    bigDes, smallDes = (vec1Des, vec2Des) if len(vec1) > len(vec2) else (vec2Des, vec1Des)
    bestGrade = -1
    bigStart = None
    smallStart = None
    bestOverlap  = None
    maximalOverlap = len(small) if maximalOverlap is None else min(len(small), maximalOverlap)
    #i iterates over the overlap size when the prefix of the merged vector is from small
    for i in reversed(xrange(minimalOverlap, maximalOverlap)):
        grade =  overLapGrader(big[:i], small[-i:], lenFac)
        if(grade > bestGrade and 
           checkDensity(density, bigDes, 0, smallDes,  len(small) - i, parts)):
            bestGrade = grade
            bigStart = 0
            smallStart = len(small) - i
            bestOverlap = i
    #i iterates over the index in big where the overlapping starts        
    startingIndexInBig = 0 if maximalOverlap == len(small) else len(big) - maximalOverlap
    for i in xrange(startingIndexInBig, len(big)-minimalOverlap):
        overlapSize = min(len(small), len(big) - i)
        grade =  overLapGrader(small[:overlapSize], big[i:i+overlapSize], lenFac)
        if(grade > bestGrade and 
           checkDensity(density, bigDes, i, smallDes,  0, parts)):
            bestGrade = grade
            bigStart = i
            smallStart = 0
            bestOverlap = overlapSize
    threshold = 0.99*averageGrade
    print 'try:', bestGrade
    print 'threshold: ', threshold
    if(bestGrade < threshold):
        return [], None, None
    print 'success'
    mergedVec= mergeByIndices(big, bigStart, small, smallStart, bestOverlap)
    mergedDes = unionSegmentDescriptor(bigDes, bigStart, smallDes, smallStart)
    return mergedVec, bestGrade, mergedDes 

def checkDensity(density, bigDes, bigStart, smallDes, smallStart, parts):
    if density is None:
        return True
    mergedDes = unionSegmentDescriptor(bigDes, bigStart, smallDes, smallStart)
    return isDescriptorLegal(parts, mergedDes, density)

def isDescriptorLegal(parts, mergedDes, density):
    layers = {}
    for partNum, partDes in mergedDes.items():
        pos = partDes[0]
        length = len(parts[partNum])
        for i in xrange(pos, pos + length):
            layers[i] = layers.get(i, 0) + 1
            if(layers[i] > density):
                return False
    return True

def mergeByIndices(big, bigStart, small, smallStart, bestOverlap):
    def toList(vec):
        return vec if type(vec) is list else vec.tolist()
    mergedVec = toList(big[:bigStart]) + \
    toList(small[:smallStart]) + \
    [(x+y)/2 for x, y in zip(big[bigStart:bigStart+bestOverlap], small[smallStart:smallStart+bestOverlap])] + \
    toList(big[bigStart+ bestOverlap:]) + \
    toList(small[smallStart + bestOverlap:])
    return mergedVec
    
def unionSegmentDescriptor(des1, off1, des2, off2):
    des = {}
    maxOrder = -1
    for segNum, (pos, order) in des1.items():
        des[segNum] = (pos + off2, order)
        maxOrder = order if order > maxOrder else maxOrder 
    for segNum, (pos, order) in des2.items():
        des[segNum] = (pos + off1, order + maxOrder +1)
    return des

def stitch(parts_p, startGrade=0.9, minimalOverlap=5, maximalOverlap=None, lenFac=0.2, density=None, 
           matchFrame=slidingOver, overLapGrader=euclidean):
    parts = copy.copy(parts_p)
    #initialize parts descriptors
    partDescriptors = []
    for i in xrange(len(parts)):
        partDescriptors.append({i:(0,0)}) # { segmentNumber: (offset, appendingTime) }
    changeWasMade = True
    grades = []
    while(changeWasMade):
        changeWasMade = False
        for i in xrange(len(parts)):
            if changeWasMade:
                break
            for j in xrange(i):
                average = startGrade if len(grades) == 0 else  np.mean(grades)
                stitched, grade, mergedDes = matchFrame(parts[i], partDescriptors[i], parts[j], \
                   partDescriptors[j], overLapGrader, minimalOverlap, maximalOverlap, average, lenFac, \
                   density, parts_p)
                if(len(stitched) == 0):
                    continue
                grades.append(grade)
                del parts[max(i,j)]
                del parts[min(i,j)]
                parts.append(stitched)
                del partDescriptors[max(i,j)]
                del partDescriptors[min(i,j)]
                partDescriptors.append(mergedDes)
                changeWasMade = True
                break
    sortingIndices = sorted(range(len(parts)), key=lambda k: len(parts[k]))
    parts = [parts[i] for i in sortingIndices]
    partDescriptors = [partDescriptors[i] for i in sortingIndices]
    return parts, partDescriptors

def plotDesBypart(originalParts, cleanedParts, mergedDes):
    des = mergedDes[-1]
    plotDes(cleanedParts, des)
    plotDes(originalParts, des)

def plotDes(parts, des): 
    sortingIndices = sorted(des.keys(), key=lambda k: des[k][1])
    frameSize = math.ceil(np.sqrt(len(sortingIndices)))
    fig = plt.figure()
    for step in xrange(1, len(sortingIndices)+1):
        curr = fig.add_subplot(frameSize, frameSize, step)
        for addedIndex in xrange(step):
            partNum = sortingIndices[addedIndex]
            part = parts[partNum]
            offset = des[partNum][0]
            curr.plot(xrange(offset, offset+len(part)),part)
                           
def plotReconstruction(cleanedParts, des):
    sortingIndices = sorted(des.keys(), key=lambda k: des[k][1])
    frameSize = math.ceil(np.sqrt(len(sortingIndices)))
    fig = plt.figure()
    whole = []
    wholeOffset = np.Inf
    for step in xrange(1, len(sortingIndices)+1):
        curr = fig.add_subplot(frameSize, frameSize, step)
        if(len(whole) > 0):
            curr.plot(xrange(wholeOffset,  wholeOffset + len(whole)), whole, c='b')
        partNum = sortingIndices[step-1]
        newAdded = cleanedParts[partNum]
        newOffset = des[partNum][0]
        newEnd = newOffset + len(newAdded)
        wholeStart = newOffset - wholeOffset if newOffset > wholeOffset else 0
        newStart =  wholeOffset - newOffset if wholeOffset > newOffset else 0
        wholeEnd = wholeOffset + len(whole)
        overlap = newEnd - wholeOffset if wholeOffset > newOffset else wholeEnd - newOffset
        if(len(whole) > 0):
            whole = mergeByIndices(whole, wholeStart, newAdded, newStart, overlap)
        else:
            whole = newAdded
        
        wholeOffset = min(wholeOffset, newOffset)
        #line, = ax.plot([], [],'r-', c='g')
        #plt.xlim(wholeOffset, len(whole))
        #plt.ylim(0, 50)
        #line_ani = animation.FuncAnimation(fig2, update_line, len(whole), \
        #fargs=( wholeOffset, whole, line), interval=50, blit=True)
        curr.plot(xrange(wholeOffset,  wholeOffset + len(whole)), whole, c='g')
        line, = curr.plot(xrange(newOffset, newEnd), newAdded, c='r')
        #an.animate(fig, line, whole)
    #fig2.axes.append(ax)

        
        
 


















      

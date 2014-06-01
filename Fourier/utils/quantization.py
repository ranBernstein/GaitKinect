import operator
import numpy as np
#from nltk.util import ngrams
import matplotlib.pyplot as plt 
import random
import periodAnalysisUtils as pe
from munkres import Munkres
import networkx as nx
from munkres import Munkres
from scipy.cluster.vq import kmeans2, kmeans
from openopt import TSP
import utils.stitching as st
import utils.interpulation as inter
from operator import add, mul
import math
import oldKinectExtractor as ke

def getEquallyWeighetedBins(values, alphabetSize = 10):
    range = np.linspace(np.min(values), np.max(values), 100000)
    hist, bins = np.histogram(values, bins=range, density=True)
    density = hist*np.diff(bins)
    threshold = 1.0/alphabetSize
    newBins = [bins[0]]
    sum = 0 
    for p, b in zip(density, bins):
        if(sum + p > threshold):
            newBins.append(b)
            sum = 0
            continue
        sum+=p
    newBins.append(bins[-1])
    return newBins

def fromStr2Vec(bins, str):
    dic = {}
    vec = []
    for i,b in enumerate(bins[:-1]):
        dic[i] =  (b + bins[i+1])/2
    for c in str:
        vec.append(dic[c])
    return vec

def createStr(bins, angles):
    strAngles = []
    for a in angles:
        for i,t in enumerate(bins):
            if a < t:
                strAngles.append(i-1)
                break
    return strAngles

def getSortedNgrams(str, n):
    ngs = list(ngrams(str,n))
    ngrams_statistics = {}
    for ngram in ngs:
        ngrams_statistics[ngram] = ngrams_statistics.get(ngram, 0) + 1
    
    ngrams_statistics_sorted = sorted(ngrams_statistics.iteritems(),\
                                key=operator.itemgetter(1),\
                                reverse=True)
    return ngrams_statistics_sorted

def findMaxNgram(str, n): 
    ngrams_statistics_sorted = getSortedNgrams(str, n)
    return ngrams_statistics_sorted[0][1]    

def plotLengthVsAmountTrafeof(angles):
    @np.vectorize
    def getMax(alphabetSize, n):
        bins = getEquallyWeighetedBins(angles, alphabetSize)
        str = createStr(bins, angles)
        return findMaxNgram(str, n)
    
    alphabetSizes = [3, 5, 7,  9, 11, 13, 15, 18]
    nSizes = [3, 5, 7,  9, 11, 13, 15, 18]
    X,Y = np.meshgrid(alphabetSizes, nSizes)
    Z = getMax( X, Y).T
    fig, ax = plt.subplots()
    p = ax.pcolor(X, Y, Z, vmin=abs(Z).min(), vmax=abs(Z).max())
    cb = fig.colorbar(p, ax=ax) 
    plt.xlabel('alphabet sizes') 
    plt.ylabel('n of the ngram') 

#plot basic atoms
def plotAtoms(bins, atoms):
    fig = plt.figure()
    def addSubPlot(atom):
        addSubPlot.counter +=1
        curr = fig.add_subplot(1,4, addSubPlot.counter)
        str = createStr(bins, atom)
        print str
        vec = fromStr2Vec(bins, str)
        plt.ylim(10,40)
        curr.plot(vec)
    addSubPlot.counter = 0
    for atom in atoms:
        addSubPlot(atom)

def sublistExists(list1, list2):
    return ''.join(map(str, list2)) in ''.join(map(str, list1))

def plotRadiusAmountRadeof(bins, ngrams_statistics_sorted):
    atom = [12, 14, 15, 17, 19, 24, 28, 33, 33, 33]
    atomStr = createStr(bins, atom)
    matches = []
    Rranges = xrange(0, 70)
    Rrands = []
    for r in Rranges:
        counter = 0
        for ng, num  in ngrams_statistics_sorted:
            diff = [np.abs(x-y) for x,y in zip(atomStr, ng)]
            currSum = np.sum(diff)
            if(r >= currSum):
                counter+=1
        matches.append(counter)
        counter2 = 0
        for i in range(len(ngrams_statistics_sorted)):
            curr = []
            for j in range(10):
                curr.append(random.randint(0,9))
            diff = [np.abs(x-y) for x,y in zip(atomStr, curr)]
            currSum = np.sum(diff)
            if(r >= currSum):
                counter2+=1
        Rrands.append(counter2)
    plt.plot(Rranges, matches, c='b', label='real data')
    plt.plot(Rranges, Rrands, c='r', label='random data')
    plt.legend().draggable()       

def getDiffSum(list1, list2):
    diff = [np.abs(x-y) for x,y in zip(list1, list2)]
    return np.sum(diff)
    
def getVecsInRadius(angles, atom, R=10, sizeOfAtom=10, alphabetSize=10):
    bins = getEquallyWeighetedBins(angles, alphabetSize)
    wholeStr = createStr(bins, angles)
    atomStr = createStr(bins, atom)
    vecs = []
    for i in range(len(wholeStr) - sizeOfAtom):
        curr = wholeStr[i:i+sizeOfAtom]
        diffSum = getDiffSum(curr, atomStr)
        if(diffSum <= R):
            vec = angles[i:i+sizeOfAtom]
            vecs.append(vec)
    return vecs

def appendAtom(atom1, atom2):
    atom1 = pe.toList(atom1)
    atom2 = pe.toList(atom2)
    last = (atom1[-1] + atom2[1])/2.0
    beforeLast = (atom1[-2] + atom2[0])/2.0
    return atom1[:-2] + [beforeLast, last] + atom2[2:]

def getDistanceBetweenAtoms(atom1, atom2):
    return np.abs(atom1[-1] - atom2[1]) + np.abs(atom1[-2] - atom2[0])

def extractPartialPattern(source, pattern):
    bestDis=np.inf 

    minimalSize = 15
    if(len(pattern) <= minimalSize or len(source) <= minimalSize):
        return None
    for i in xrange(len(pattern)):
        for j in xrange(i+15, len(pattern)):
            partialPattern = pattern[i:j]
            dis, partOffset, _, _ = simpleDis(source, partialPattern)
            dis -= len(partialPattern)*0.2
            if(dis < bestDis):
                bestDis = dis
                bestPartOffset = partOffset
                bestVec = source[partOffset:(partOffset+len(partialPattern))]
                bestPattern = partialPattern
                bestPatternOffset = i
    return bestDis, bestPartOffset, bestPattern, bestPatternOffset

def simpleDis(part, currAtom):
    bestDis = np.inf
    bestOffset = 0
    for i, v in enumerate(part[:(-len(currAtom)+1)]):
        dis = 0
        for j, v in enumerate(currAtom):
            dis += np.abs(part[i + j] -  currAtom[j])**2
        dis /= len(currAtom)
        dis = math.sqrt(dis)
        if(dis < bestDis):
            bestDis = dis
            bestOffset = i
    return bestDis, bestOffset, currAtom, 0

def getAtomFromFrac(part, atom, sizeFactor=2, minimalFracSize=15):
    verticalTranslations = [10, 0, -10]
    scales = [0.7, 1, 1.2]
    temporalScales =  [0.85, 1, 1.2, 1.45]
    bestMatch = part[:len(atom)]
    bestDis = np.inf
    bestBias = None
    bestScale = 1
    dis = np.inf
    for bias in verticalTranslations:
        for scale in scales:
            for  scaleFactor in temporalScales:       
                currAtom = [scale*x for x in atom]
                currAtom = inter.scaleVec(currAtom, scaleFactor)
                currAtom =  map(add, [bias]*len(currAtom), currAtom)
                costs = {}
                minimalOverlap = minimalFracSize
                for i in range(len(part)-minimalOverlap+1):
                    for j in range(len(currAtom)-minimalOverlap+1):
                        tmp=0
                        for k in range(minimalOverlap):
                            tmp+=np.abs(part[i+k] - currAtom[j+k])
                        costs[(i,j,minimalOverlap-1)] = tmp/(minimalOverlap**sizeFactor)
                        for size in range(minimalOverlap, min(len(part), len(currAtom))):
                            if j+size>len(currAtom) or i+size>len(part):
                                break
                            d = np.abs(part[i+size-1] - currAtom[j+size-1])
                            costs[(i,j,size)] = (costs[(i,j,size-1)]*((size-1)**sizeFactor)+d)/(size**sizeFactor) - size/5000.0
                            if costs[(i,j,size)] < dis:
                                dis = costs[(i,j,size)]
                                offset = i
                                pattern = currAtom[j:j+size]
                                bestPartialPatternOffset = j
                                bestDis = dis
                                
                                bestMatch = part[offset:offset+len(pattern)]
                                bestBias = bias
                                bestScale = scale
                                bestTemporalScale = scaleFactor
                                bestAtom = pattern
                                bestOffset = offset
                                """
                                if dis < 0.02:
                                    plt.title(dis)
                                    plt.plot(currAtom[j:j+size])
                                    plt.plot(part[i:i+size])
                                    plt.show()
                                    pass
                                """
                """
                retVal = calcDis(part, currAtom)
                if retVal is not None:
                    dis, offset, pattern, patternOffset = retVal
                else:
                    continue
                if(dis < bestDis):
                    bestDis = dis
                    bestMatch = part[offset:offset+len(pattern)]
                    bestBias = bias
                    bestScale = scale
                    bestTemporalScale = scaleFactor
                    bestAtom = pattern
                    bestOffset = offset
                    bestPartialPatternOffset = patternOffset
                """
    if(bestBias is None):
        return None
    return bestMatch, bestDis, bestAtom, bestBias, bestScale, bestTemporalScale, \
        bestOffset, bestPartialPatternOffset
                                                
def createClustersAndMatchingMatrices(parts, atoms, numOfClusters, disFactor):
    vecs = []
    mats = []
    for atom in atoms:
        closeVectors = []
        tmp = []
        fig = plt.figure()
        i=1
        for part in parts:
            retVal = getAtomFromFrac(part, atom, simpleDis)
            if retVal is None:
                continue
            frac,  dis, vecAtom, bias, bestScale, temporalScale, offset, _= retVal
            tmp.append((dis, frac))
            amplitude = np.max(vecAtom) - np.min(vecAtom)
            if(dis > amplitude*disFactor):
                continue
            closeVectors.append(frac)
            if(i>25):
                continue
            curr = fig.add_subplot(5,5,i)
            i+=1
            
            plt.title('bias: ' + str(bias) + ' scale: ' + str(bestScale) + 
                ' bestTemporalScale: ' + str(temporalScale) + ' dis: ' + str(dis))
            curr.plot(part, c='b')
            rng = xrange(offset, offset + len(frac))
            curr.plot(rng, vecAtom, c='g')
            curr.plot(rng, frac, c='r')
            #plt.show()
        print len(tmp), len(closeVectors)
        if(len(closeVectors) < numOfClusters):
            tmp = sorted(tmp, key=lambda tup: tup[0])
            clusteredVectors = [t[1] for t in tmp[:numOfClusters]]
        else:
            lengthCounter = {}
            for vec in closeVectors:
                lengthCounter[len(vec)] = lengthCounter.get(len(vec), []) + [vec]
            residum = len(closeVectors)%numOfClusters
            clusteredVectors = []
            tmpNumOfClusters = numOfClusters
            last = len(lengthCounter) - 1
            for i, (vecLen, sameLengthVecs) in enumerate(lengthCounter.items()):
                #if(vecLen <= len(sameLengthVecs)):
                    #sameLengthVecs, idx = kmeans2(np.array(sameLengthVecs), max(1, int(float(numOfClusters)*vecLen/len(closeVectors))))
                numOfClusterPerLength = int(round(float(numOfClusters)*len(sameLengthVecs)/len(closeVectors)))
                numOfClusterPerLength = min(numOfClusterPerLength, tmpNumOfClusters) if i!=last else tmpNumOfClusters
                tmpNumOfClusters -= numOfClusterPerLength
                if(numOfClusterPerLength == 0):
                    continue
                sameLengthVecs, idx = kmeans(np.array(sameLengthVecs), numOfClusterPerLength)
                for v in sameLengthVecs:
                    clusteredVectors.append(pe.toList(v))
                #clusteredVectors = clusteredVectors + sameLengthVecs

        vecs.append(pe.toList(clusteredVectors))
        if(len(vecs) > 1):
            last = vecs[-2]
            mat = []
            for atom1 in last:
                row = []
                for atom2 in clusteredVectors:
                    row.append(getDistanceBetweenAtoms(atom1, atom2))
                mat.append(row)
            mats.append(mat)
        if(len(vecs)==len(atoms)):
            next = vecs[0]
            mat = []
            for atom1 in clusteredVectors:
                row = []
                for atom2 in next:
                    row.append(getDistanceBetweenAtoms(atom1, atom2))
                mat.append(row)
            mats.append(mat)  
    return vecs, mats

def createStridesFromAtoms(mats, vecs): 
    m = Munkres()
    strides = vecs[0]
    for i,mat in enumerate(mats[:-1]):
        indexes = m.compute(mat)
        for row, col in indexes:
            #try:
            if(row < len(strides)):
                strides[row] = appendAtom(strides[row], vecs[(i+1)][col])
            #except Exception, e:
            #   pass
    return strides

def orderWithCost(strides, costFunc=getDistanceBetweenAtoms, appendFunc=appendAtom):
    N = len(strides)
    G = nx.DiGraph()
    nodes=[(i1,i2,{'cost':costFunc(stride1, stride2)}) for i1,stride1 in enumerate(strides) for i2,stride2 in enumerate(strides) if i1 != i2]
    G.add_edges_from(nodes)
    objective = lambda values: values['cost'] 
    p = TSP(G, objective = objective,  start = 0, returnToStart=False, fTol=100*N)
    r = p.solve('interalg') 
    print(r.nodes)
    print(r.edges) # (node_from, node_to)
    print(r.Edges) # full info on edges; unavailable for solver sa yet
    whole = strides[r.nodes[0]]
    for n in r.nodes[1:]:
        whole = appendFunc(whole, strides[n])
    return whole 


    
def doRambamAlgo(time, values, numOfClusters, disFactor=0.2):
    atoms = [
             [14, 15, 17, 19, 24, 28, 33, 33, 33, 33],
             [33, 33, 33, 33, 28, 24, 19, 17, 15, 14],
             [15, 14, 12, 12, 14, 15, 16, 17.5, 17.5, 17.5],
             [17.5, 17.5, 16, 15, 14, 13, 12, 12, 14, 15]
        ]
    minimalCluster = len(atoms[0])
    fracs = ke.clusterByTime(time, values, False, minimalCluster)
    #originalFracs = copy.deepcopy(fracs)
    prob = 0.05
    fracs = ke.filterOutliers(fracs, False, prob)
    i=0
    parts, kuku = ke.cleanFracs(fracs, False)
    vecs, mats = createClustersAndMatchingMatrices(parts, atoms, numOfClusters, disFactor)
    strides = createStridesFromAtoms(mats, vecs)
    if(numOfClusters > 2):
        whole = orderWithCost(strides)
        
        xlabel = 'Frames(each frame is 33 miliseconds)'
        ylabel = 'Right knee angle (in degrees)'
        st.plotParts(strides, xlabel, ylabel, xrange(len(strides)))
        
    else: 
        if(numOfClusters == 2) :
            byOrderDis = getDistanceBetweenAtoms(strides[0], strides[1])
            byOrder = appendAtom(strides[0], strides[1])
            inverseDis = getDistanceBetweenAtoms(strides[1], strides[0])
            inverse = appendAtom(strides[1], strides[0])
            whole = byOrder if byOrderDis < inverseDis else inverse
        else:
            whole = strides[0]
    return whole
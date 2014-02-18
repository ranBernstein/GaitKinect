import operator
import numpy as np
#from nltk.util import ngrams
import matplotlib.pyplot as plt 
import random
import periodAnalysisUtils as pe
from munkres import Munkres
import networkx as nx
from munkres import Munkres
from scipy.cluster.vq import kmeans2
from openopt import TSP

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

def fusionByMaximumMatch(parts):
    mat = []
    for atom1 in parts:
        row = []
        for atom2 in parts:
            row.append(getDistanceBetweenAtoms(atom1, atom2))
        mat.append(row)
    m = Munkres()
    

def createClustersAndMatchingMatrices(parts, atoms, radius, sizeOfAtom, alphabetSize, numOfClusters):
    vecs = []
    mats = []
    for atom in atoms:
        vec = []
        for part in parts:          
            vec += getVecsInRadius(part, atom, radius, sizeOfAtom, alphabetSize)
        print len(vec)
        res, idx = kmeans2(np.array(vec), numOfClusters)
        vecs.append(pe.toList(res))
        if(len(vecs) > 1):
            last = vecs[-2]
            mat = []
            for atom1 in last:
                row = []
                for atom2 in res:
                    row.append(getDistanceBetweenAtoms(atom1, atom2))
                mat.append(row)
            mats.append(mat)
        if(len(vecs)==len(atoms)):
            next = vecs[0]
            mat = []
            for atom1 in res:
                row = []
                for atom2 in next:
                    row.append(getDistanceBetweenAtoms(atom1, atom2))
                mat.append(row)
            mats.append(mat)  
    return vecs, mats

def createStridesFromAtoms(mats, atoms): 
    m = Munkres()
    strides = atoms[0]
    for i,mat in enumerate(mats[:-1]):
        indexes = m.compute(mat)
        for row, col in indexes:
            strides[row] = appendAtom(strides[row], atoms[(i+1)][col])
    return strides

def orderWithCost(strides):
    N = len(strides)
    G = nx.DiGraph()
    nodes=[(i1,i2,{'cost':getDistanceBetweenAtoms(stride1, stride2)}) for i1,stride1 in enumerate(strides) for i2,stride2 in enumerate(strides) if i1 != i2]
    G.add_edges_from(nodes)
    objective = lambda values: values['cost'] 
    p = TSP(G, objective = objective,  start = 0, returnToStart=False, fTol=11*N)
    r = p.solve('interalg') 
    print(r.nodes)
    print(r.edges) # (node_from, node_to)
    print(r.Edges) # full info on edges; unavailable for solver sa yet
    whole = strides[r.nodes[0]]
    for n in r.nodes[1:]:
        whole = appendAtom(whole, strides[n])
    return whole 

#get common patterns
"""
fig = plt.figure()
for i in range(49):
    mostCommon = ngrams_statistics_sorted[i][0]
    curr = fig.add_subplot(7,7,i+1)
    amount = ngrams_statistics_sorted[i][1]
    plt.title(amount)
    vec = qu.fromStr2Vec(bins, mostCommon)
    curr.plot(vec)
"""
"""
plt.hist(angles, bins=100)
plt.title('Uniform bins')
plt.xlabel('Bin index')
plt.ylabel('Amount of values')
plt.xlim(0,100)
"""


"""
plt.figure()
plt.hist(angles, bins=newBins)
plt.title('Equally distributed bins')
plt.xlabel('Bin index')
plt.ylabel('Amount of values')
"""


import numpy as np
import matplotlib.pyplot as plt
import itertools
import random
import copy
import interpulation

def isEqual(a, b, gap=0):
    #return a==b
    epsilon = np.abs(float(a+b)/1000.0)
    if(gap == 0):
        return np.abs(a-b) <=  epsilon
    if(np.abs(gap) > 3*epsilon):
        return False
    return np.abs(a - b - gap) <=  epsilon

def compareHashed(t1, t2):
    try:
        some_object_iterator = iter(t1)
    except TypeError, te:
        return isEqual(t1, t2)
    #t1 and t2 are iterables
    for e1, e2 in zip(t1, t2):
        if(not isEqual(e1, e2)):
            return False
    return True

def myHash(seq):
    return seq
    return hash(tuple(seq))
    #return seq[0], seq[-1], np.mean(seq), np.std(seq)

def shift(l, n):
    return l[n:] + l[:n]     
    
    
def getAMCperiod(joint, file):
    f=None
    try:
        f = open(file, 'r')
    except IOError:
        return []
    input = []
    for line in f:
        if joint in line:
            input.append(float(line.split()[1]))
    return input


def cost(vec):
    #Fourier
    """
    trans = np.fft.fft(vec)
    absTrans = np.absolute(trans)
    absTrans.sort()
    coeffAmount = 13
    mainSum=0
    for i in xrange(1, min(coeffAmount+1, len(absTrans))):
        mainSum += absTrans[-i]
    return mainSum/np.sum(absTrans)
    """
    sum=0.0
    for i in xrange(len(vec)-1):
        sum+= (vec[i+1] - vec[i])**2
    return float(len(vec))**2 / sum   
                
t = np.linspace(0.0, 2*np.pi, num=100)
subject = 2
sample = 1
file = 'AMCs/subjects/' + str(subject) + '/origin1-2.amc'  
#file = 'AMCs/subjects/' + str(subject) + '/' + str(sample) + '.amc'
joint = 'ltibia'
input = getAMCperiod(joint, file)
partsAmount = 18
parts = []
partsIndices = xrange(partsAmount)
chunckSize = len(input)/partsAmount
prefixes = {}
sufixes = {}
overlapFactor = 3
for i in partsIndices:
    start = max(0, i*chunckSize-random.randint(1, int(overlapFactor*chunckSize)))
    end = min((i+2)*chunckSize+random.randint(1, int(overlapFactor*chunckSize)), len(input))
    part = input[start:end]
    #print 'start: ' + str(start) + ' end: ' + str(end)
    parts.append(part)
    for j in xrange(1,len(part)):
        prefixes[(i,j)] = myHash(tuple(part[:j]))
        sufixes[(i,j)] = myHash(tuple(part[len(part)-j:])) 
    
def appendFrac(whole, originalNext):
    scaledNexts = interpulation.getScaledVectors(originalNext)
    longestOverlap = 0
    bestExtention = None
    for next in scaledNexts: 
        for j in reversed(xrange(1,len(next))):
            if(j > len(whole)-1):
                continue
            #if(compareHashed(prefixes[(nextIndex, j)], sufixes[(lastIndex, j)])):
                #averaging
                #for i in xrange(j):
                #   whole[i] = (whole[-i] + next[j-i])/2
                #return whole + next[j:]
            match = True
            gap = np.mean(whole[-j:]) - np.mean(next[:j])
            for i in xrange(j):
                if(not isEqual(whole[-j+i], next[i], gap)):
                    match = False
                    break
            if(match and j>longestOverlap):
                longestOverlap = j
                bestExtention = next[j:]
        #return whole + next
        #force continuty
    if(bestExtention is not None):
        return whole + bestExtention.tolist()
    return whole

def prependFrac(whole, next):
    for j in reversed(xrange(1,len(next))):
        if(j > len(whole)-1):
            continue
        match = True
        gap = np.mean(whole[:j]) - np.mean(next[-j:])
        for i in xrange(j):
            if(not isEqual(whole[i], next[-j+i], gap)):
                match = False
                break
        if(match):
            return next[:-j] + whole 
    return whole

def foldEdge(whole):
    maxLen = len(whole)/2
    for i in reversed(xrange(1, maxLen)):
        match = True
        gap = myHash(whole[:i]) - myHash(whole[-i:])
        for j in xrange(i):
            if(not isEqual(whole[j], whole[-i+j], gap)):
                match = False
                break
        if(match):
            whole = whole[i:]
            return whole
    return whole

"""
allPerms = list(itertools.permutations(partsIndices))
bestVec = []
bestGrade = 0
first = True
firstVec = None
for perm in allPerms:
    whole = copy.copy(parts[perm[0]])
    for i in perm[1:]:
        whole = appendFrac(whole, parts[i])
    
    #folding to one stride
    #chopped = foldEdge(whole)
    #while(len(chopped) < len(whole)):
    #    whole = chopped
    #    chopped = foldEdge(whole)
    

    if(first):
        firstVec = whole
        first = False
    grade = cost(whole)
    if(grade>bestGrade):
        print perm, grade, len(whole), cost(whole[:123])
        bestGrade = grade
        bestVec = whole
"""
byOrder = copy.copy(parts[0])
for part in parts[1:]:
    byOrder = appendFrac(byOrder, part)
      
#greedy
parts.sort()
parts.reverse()
greedy = copy.copy(parts[0])
notUsed = []
for part in parts[1:]:
    lenBefore = len(greedy)
    greedy = appendFrac(greedy, part)
    if(lenBefore == len(greedy)):
        notUsed.append(part)
# plt.figure()
# plt.plot(xrange(len(greedy)), greedy, color='red')
    
counter =0
for part in notUsed:
    lenBefore = len(greedy)
    greedy = prependFrac(greedy, part)
    if(len(greedy) != lenBefore):
        counter+=1
print len(notUsed) -  counter


#offset = input.index(max(input)) - bestVec.index(max(bestVec))
#bestVec = shift(bestVec,-offset)

#offset = input.index(max(input)) - greedy.index(max(greedy))
#greedy = shift(greedy,-offset)
#plt.plot(xrange(len(bestVec)), bestVec, color='red')
plt.figure()
plt.plot(xrange(len(input)), input, color='blue')
plt.figure()
plt.plot(xrange(len(byOrder)), byOrder, color='green')
plt.figure()
plt.plot(xrange(len(greedy)), greedy, color='black')


"""
for part in parts:
    plt.figure()
    plt.plot(xrange(len(part)), part)
"""
plt.show()
  
    
    
    
    
    
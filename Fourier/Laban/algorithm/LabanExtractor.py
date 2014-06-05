import utils.angleExtraction as ae
import matplotlib.pyplot as plt
import utils.MovingAverage as ma
import numpy as np
from scipy.ndimage.filters import maximum_filter
import utils.spikeDetection as spike
import utils.periodAnalysisUtils as pu

class LabanExtractor:
        
    def extractLaban(self, fileName, huristic):
        f = open(fileName, 'r')
        headers = f.readline().split()
        jointsIndices = self.getJointsIndices(headers)
        vec = []
        for line in f:
            lineInFloats=[float(v) for v in line.split()]
            vec.append(huristic(lineInFloats, headers, jointsIndices))
        return vec
    
    def printConfedence(self, filtered, ranges, positive, negetive):
        print ranges
        m = np.mean(filtered)
        amplitude = max(filtered)-min(filtered)
        for openIndex, close, type in ranges:
            if type==1:
                confidence = (filtered[close] - filtered[openIndex])/amplitude
                print positive, ' with confidence of ', confidence
                continue
            if type==-1:
                confidence = (filtered[openIndex]-filtered[close])/amplitude
                print negetive, ' with confidence of ', confidence
                
    def prepareRanges(self, clustersByPercentilies):
        ranges = []
        currClusOpen, currClusClose, currCluster = 0,0,0
        for i,v in enumerate(clustersByPercentilies):
            if currCluster!=v:
                ranges.append((currClusOpen, currClusClose, currCluster))
                currClusOpen=i
                currClusClose=i
                currCluster=v
                continue
            currClusClose+=1
        return ranges
    
    def plotResults(self, vec, positive, negetive):
        plt.figure()
        #plt.plot(vec)
        filtered = ma.movingAverage(vec, 50, 1.0)
        #plt.plot(filtered)
        filtered = pu.normalizeVector(filtered)
        plt.plot(filtered)
        change = [filtered[i+1]-filtered[i] for i in range(len(filtered)-1)]
        change = ma.movingAverage(change, 75, 1.0)
        change = pu.normalizeVector(change)
        plt.plot(change)
        #plt.figure()
        clustersByPercentilies = spike.clusterByPercemtile(change, 700, 80)
        plt.plot(clustersByPercentilies)
        clustersByPercentilies = pu.smoothOutliers(clustersByPercentilies)
        plt.plot(clustersByPercentilies)
        #plt.figure()
        ranges = self.prepareRanges(clustersByPercentilies)
        self.printConfedence(filtered, ranges, positive, negetive)
        plt.show()    
    
    def expendingCondencingWrapper(self, lineInFloats, headers, jointsIndices):
        return ae.calcAverageJointDistanceFromCenter(lineInFloats, jointsIndices)
    
    def plotExpendingCondencing(self, fileName):
        input = self.extractLaban(fileName, self.expendingCondencingWrapper)
        self.plotResults(input, 'Expanding', 'Condensing')
         
    def spreadindAndClosingWrapper(self, lineInFloats, headers, jointsIndices):
        return ae.calcAverageDistanceOfIndicesFromLine(lineInFloats, \
                        jointsIndices, *self.getLongAxeIndices(headers))
    
    def plotSpreadindAndClosing(self, fileName):
        input = self.extractLaban(fileName, self.spreadindAndClosingWrapper)
        self.plotResults(input, 'Spreading', 'Closing')
        
    def risingAndSinkingWrapper(self, lineInFloats, headers, jointsIndices):
        return ae.jointsMovementInDirection(lineInFloats, jointsIndices, [0,1,0])
    
    def plotRisingAndSinking(self, fileName):
        input = self.extractLaban(fileName, self.risingAndSinkingWrapper)
        self.plotResults(input, 'Rising', 'Sinking')
    
    #def directAndUndirect(self, lineInFloats, headers, jointsIndices):
        #return ae.jointsMovementInDirection(lineInFloats, jointsIndices, [0,1,0])
    
    """
    def plotDirectAndUndirect(self, filenNme):
        #input = self.extractLaban(fileName, self.risingAndSinkingWrapper)
        #self.plotResults(input, 'Rising', 'Sinking')
        f = open(fileName, 'r')
        headers = f.readline().split()
        jointsIndices = self.getJointsIndices(headers)
        frontDirections = []
        centers = []
        for line in f:
            lineInFloats=[float(v) for v in line.split()]
    """
    
    def plotadvanceAndRetreate(self, fileName):
        f = open(fileName, 'r')
        headers = f.readline().split()
        jointsIndices = self.getJointsIndices(headers)
        frontDirections = []
        centers = []
        for line in f:
            lineInFloats=[float(v) for v in line.split()]
            centers.append(ae.calcJointsAverage(lineInFloats, jointsIndices))
            shouldersVecOnXZPlan = ae.getVecBetweenJoints(headers, lineInFloats,\
                                   'ShoulderRight_X', 'ShoulderLeft_X')
            #frontDirections.append([-shouldersVecOnXZPlan[2], 0 , shouldersVecOnXZPlan[0]])
            frontDirections.append([1,0,0])
        plt.figure()
        plt.plot(centers)
        frontDirections = zip(*ma.partsmovingAverage(zip(*frontDirections), 50, 1))
        plt.figure()
        plt.plot(frontDirections)
        
        movingDirections = np.diff(centers, axis=0)
        movingDirections = zip(*ma.partsmovingAverage(zip(*movingDirections), 50, 1))
        advancements = []
        for front, move in zip(frontDirections[:-1], movingDirections):
            if np.abs(front[0])/np.abs(front[2]) > 2:
                front = [ae.length(front),0,0]
            product = np.dot(front, move)
            advancements.append(product)
        advancements = ma.movingAverage(advancements, 50, 1)
        advancements = pu.normalizeVector(advancements)
        clustersByPercentilies = spike.clusterByPercemtile(advancements,1000, 75)
        clustersByPercentilies = pu.smoothOutliers(clustersByPercentilies)
        plt.figure()
        plt.plot(clustersByPercentilies)
        #advancements = pu.normalizeVector(advancements)
        plt.plot(advancements)
        ranges = self.prepareRanges(clustersByPercentilies)
        self.printConfedence(advancements, ranges, 'Advancing', 'Retreating')
        plt.show()
           
class LabanExtractorKinectV1(LabanExtractor) :
    
    def getJointsIndices(self, headers):
        numOfJoints = (len(headers)-2)/4
        return [2+4*index for index in range(numOfJoints)]
    
    def getLongAxeIndices(self, headers):
        return headers.index('HipCenter_X'), headers.index('ShoulderCenter_X')
        
#plotExpendingCondencing()
#plotSpreadindAndClosing()
#plotRisingAndSinking()
#plotadvanceAndRetreate()
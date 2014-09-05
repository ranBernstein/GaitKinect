import matplotlib.pyplot as plt
import utils.MovingAverage as ma
import numpy as np
import utils.spikeDetection as spike
import utils.utils as pu
import utils.kinect.jointsMap as jm

class LabanExtractor:
        
    def extractLaban(self, fileName, huristic):
        f = open(fileName, 'r')
        headers = f.readline().split()
        headers = jm.getFileHeader(headers)
        jointsIndices = self.getJointsIndices(headers)
        vec = []
        for line in f:
            lineInFloats=[float(v) for v in line.split()]
            #try:
            vec.append(huristic(lineInFloats, headers, jointsIndices))
            #except Exception, e:
                #vec.append(huristic(lineInFloats, headers, jointsIndices))
                #print e
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
    
    
           
    def getJointsIndices(self, headers):
        numOfJoints = (len(headers)-2)/4
        return [2+4*index for index in range(numOfJoints)]
    
class LabanExtractorKinectV1(LabanExtractor) :
    def getLongAxeIndices(self, headers):
        return headers.index('HipCenter_X'), headers.index('ShoulderCenter_X')
    def getCenterJointIndex(self, headers):
        return headers.index('HipCenter_X')
    
class LabanExtractorKinectV2(LabanExtractor) :
    def getLongAxeIndices(self, headers):
        return headers.index('SpineBase_X'), headers.index('SpineShoulder_X')
    def getCenterJointIndex(self, headers):
        return headers.index('SpineBase_X')   
#plotExpendingCondencing()
#plotSpreadindAndClosing()
#plotRisingAndSinking()
#plotadvanceAndRetreate()
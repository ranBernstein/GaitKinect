from Laban.LabanUtils import AbstractLabanAnalyzer
from Laban.LabanUtils import AbstractAnalysis
import utils.kinect.angleExtraction as ae
import utils.MovingAverage as ma
import numpy as np
import utils.kinect.jointsMap as jm

class AdvanceAndRetreate(AbstractAnalysis.AbstractAnalysis):
    
    def getPositiveAndNegetive(self):
        return 'Advance', 'Retreate'
    
    #def wrapper(self, lineInFloats, headers, jointsIndices):
     #   return ae.jointsMovementInDirection(lineInFloats, jointsIndices, [0,1,0])
    
    def extract(self, fileName):
        f = open(fileName, 'r')
        headers = f.readline().split()
        headers = jm.getFileHeader(headers)
        jointsIndices = self.extractor.getJointsIndices(headers)
        frontDirections = []
        centers = []
        sholderVec = []
        for line in f:
            lineInFloats=[float(v) for v in line.split()]
            centers.append(ae.calcJointsAverage(lineInFloats, jointsIndices))
            shouldersVecOnXZPlan = ae.getVecBetweenJoints(headers, lineInFloats,\
                                   'ShoulderRight_X', 'ShoulderLeft_X')
            #sholderVec.append(shouldersVecOnXZPlan)
            frontDirections.append([shouldersVecOnXZPlan[2], 0 , -shouldersVecOnXZPlan[0]])
            #frontDirections.append([1,0,0])
        frontDirections = zip(*ma.partsmovingAverage(zip(*frontDirections), 50, 1))
        movingDirections = np.diff(centers, axis=0)
        movingDirections = zip(*ma.partsmovingAverage(zip(*movingDirections), 50, 1))
        advancements = []
        for front, move in zip(frontDirections[:-1], movingDirections):
            if np.abs(front[0])/np.abs(front[2]) > 2:
                front = [ae.length(front),0,0]
            product = np.dot(front, move)
            advancements.append(product)
        return advancements
        """
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
        """  
def analyze(inputFile):
    extractor = AbstractLabanAnalyzer.getExtractor(inputFile)
    analysis = AdvanceAndRetreate(extractor)
    return analysis.extract(inputFile)
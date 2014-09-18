from Laban.LabanUtils import AbstractLabanAnalyzer
from Laban.LabanUtils import AbstractAnalysis
import utils.kinect.angleExtraction as ae
import numpy as np

class LightAndStrong(AbstractAnalysis.AbstractAnalysis):
    
    def getPositiveAndNegetive(self):
        return 'Strong', 'Light'   
    
    def extract(self, fileName):
        data, headers = ae.fromFileToFloats(fileName)
        jointsIndices = self.extractor.getJointsIndices(headers)
        centerXIndex = self.extractor.getCenterJointIndex(headers)
        dataRelativeToCenter = ae.subCenterFromDataForIndecies(data, centerXIndex, jointsIndices)
        velocities = np.diff(dataRelativeToCenter,1, 0)
        sqVelocities = np.square(velocities)   
        energy = [np.sum(line) for line in sqVelocities]
        return energy

def analyze(inputFile):
    extractor = AbstractLabanAnalyzer.getExtractor(inputFile)
    analysis = LightAndStrong(extractor)
    return analysis.extract(inputFile)

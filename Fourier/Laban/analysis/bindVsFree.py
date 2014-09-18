from Laban.LabanUtils import AbstractLabanAnalyzer
from Laban.LabanUtils import AbstractAnalysis
import utils.kinect.angleExtraction as ae
import numpy as np

class FreeAndBind(AbstractAnalysis.AbstractAnalysis):
    
    def getPositiveAndNegetive(self):
        return 'free', 'bind'   
    
    def extract(self, fileName):
        data, headers = ae.fromFileToFloats(fileName)
        jointsIndices = self.extractor.getJointsIndices(headers)
        centerXIndex = self.extractor.getCenterJointIndex(headers)
        dataRelativeToCenter = ae.subCenterFromDataForIndecies(data, centerXIndex, jointsIndices)
        velocities = np.diff(dataRelativeToCenter,1, 0)[1:]
        accelarations = np.diff(velocities,1, 0)
        #h = [np.sum(np.abs(line))*np.sum(acc) for acc,line in zip(velocities, accelarations)]
        h = [np.sum(np.abs(line)) for line in velocities]
        return h

def analyze(inputFile):
    extractor = AbstractLabanAnalyzer.getExtractor(inputFile)
    analysis = FreeAndBind(extractor)
    return analysis.extract(inputFile)

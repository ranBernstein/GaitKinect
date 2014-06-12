
from  Laban import AbstractLabanAnalyzer, AbstractAnalysis
import utils.angleExtraction as ae

class ExpendingCondencing(AbstractAnalysis.AbstractAnalysis):
    
    def getPositiveAndNegetive(self):
        return 'Expanding', 'Condencing'
    
    def wrapper(self, lineInFloats, headers, jointsIndices):
        return ae.calcAverageJointDistanceFromCenter(lineInFloats, jointsIndices)
        

def analyze(inputFile):
    extractor = AbstractLabanAnalyzer.getExtractor(inputFile)
    analysis = ExpendingCondencing(extractor)
    return analysis.extract(inputFile)

"""
    def expendingCondencingWrapper(self, lineInFloats, headers, jointsIndices):
        return ae.calcAverageJointDistanceFromCenter(lineInFloats, jointsIndices)
    
    def extractExpendingCondencing(self, fileName):
        return self.extractLaban(fileName, self.expendingCondencingWrapper)
    
    def plotExpendingCondencing(self, fileName):
        input = self.extractLaban(fileName, self.expendingCondencingWrapper)
        self.plotResults(input, 'Expanding', 'Condensing')
"""
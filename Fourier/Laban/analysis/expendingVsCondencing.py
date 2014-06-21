
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

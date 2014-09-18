from Laban.LabanUtils import AbstractLabanAnalyzer
from Laban.LabanUtils import AbstractAnalysis
import utils.kinect.angleExtraction as ae

class SpreadindAndClosing(AbstractAnalysis.AbstractAnalysis):
    
    def getPositiveAndNegetive(self):
        return 'Spreading', 'Closing'
    
    def wrapper(self, lineInFloats, headers, jointsIndices):
        return ae.calcAverageDistanceOfIndicesFromLine(lineInFloats, \
                    jointsIndices, *self.extractor.getLongAxeIndices(headers))
        

def analyze(inputFile):
    extractor = AbstractLabanAnalyzer.getExtractor(inputFile)
    analysis = SpreadindAndClosing(extractor)
    return analysis.extract(inputFile)

"""
def spreadindAndClosingWrapper(extractor, lineInFloats, headers, jointsIndices):
    return ae.calcAverageDistanceOfIndicesFromLine(lineInFloats, \
                    jointsIndices, *extractor.getLongAxeIndices(headers))
    
def extractSpreadindAndClosing(extractor, fileName):
    return extractor.extractLaban(fileName, extractor.spreadindAndClosingWrapper)

def plotSpreadindAndClosing(extractor, fileName):
    input = extractor.extractLaban(fileName, extractor.spreadindAndClosingWrapper)
    extractor.plotResults(input, 'Spreading', 'Closing')
"""
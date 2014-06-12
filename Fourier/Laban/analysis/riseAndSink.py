from  Laban import AbstractLabanAnalyzer, AbstractAnalysis
import utils.angleExtraction as ae

class RiseAndSink(AbstractAnalysis.AbstractAnalysis):
    
    def getPositiveAndNegetive(self):
        return 'Spreading', 'Closing'
    
    def wrapper(self, lineInFloats, headers, jointsIndices):
        return ae.jointsMovementInDirection(lineInFloats, jointsIndices, [0,1,0])
        
def analyze(inputFile):
    extractor = AbstractLabanAnalyzer.getExtractor(inputFile)
    analysis = RiseAndSink(extractor)
    return analysis.extract(inputFile)

"""
def risingAndSinkingWrapper(self, lineInFloats, headers, jointsIndices):
    return ae.jointsMovementInDirection(lineInFloats, jointsIndices, [0,1,0])

def plotRisingAndSinking(self, fileName):
    input = self.extractLaban(fileName, self.risingAndSinkingWrapper)
    self.plotResults(input, 'Rising', 'Sinking')
"""
class AbstractAnalysis:
    def __init__(self, extractor):
        self.extractor = extractor
        
    def wrapper(self, lineInFloats, headers, jointsIndices):
        raise 'Not implemented'
    
    def extract(self, fileName):
        return self.extractor.extractLaban(fileName, self.wrapper)
    
    def getPositiveAndNegetive(self):
        raise 'Not implemented'
    
    def plot(self, fileName):
        input = self.extract(fileName)
        self.extractor.plotResults(input, *self.getPositiveAndNegetive())
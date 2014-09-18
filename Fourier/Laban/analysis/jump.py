from Laban.LabanUtils import AbstractLabanAnalyzer
from Laban.LabanUtils import AbstractAnalysis
import utils.kinect.angleExtraction as ae
import utils.kinect.jointsMap as jm
import numpy as np

class Jump(AbstractAnalysis.AbstractAnalysis):
    
    def getPositiveAndNegetive(self):
        return 'Spreading', 'Closing'
    
    def wrapper(self, lineInFloats, headers, jointsIndices):
        
        return ae.calcAverageDistanceOfIndicesFromLine(lineInFloats, \
                    jointsIndices, *self.extractor.getLongAxeIndices(headers))
        

def analyze(inputFile):
    f = open(file, 'r')
    headers = f.readline()
    headers = jm.getFileHeader(headers)
    jumpsLeft = []
    jumpsRight = []
    for line in f:
        lineInFloats=[float(v) for v in line.split()]
        indexRight = headers.index('AnkleRight_Y')
        indexLeft = headers.index('AnkleLeft_Y')
        jumpsLeft.append(lineInFloats[indexLeft])
        jumpsRight.append(lineInFloats[indexRight])
    jumpsLeft = np.abs(np.diff(jumpsLeft))
    jumpsRight = np.abs(np.diff(jumpsRight))
    return [np.mean([l, r] for l, r in zip(jumpsLeft, jumpsRight))]
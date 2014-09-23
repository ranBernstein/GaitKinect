from utils.kinect import jointsMap
from Laban.algorithm import LabanExtractor as le

#class AbstractLabanAnalyzer:
def getExtractor(inputFile):
    f = open(inputFile, 'r')
    headers = f.readline().split()
    ver = jointsMap.getVersion(headers)
    if ver == 'OLD':
        return le.LabanExtractorKinectV1()
    else:
        return le.LabanExtractorKinectV2()

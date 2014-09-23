from Laban.algorithm import LabanExtractor as le

extractor = le.LabanExtractorKinectV1()

#fileName = 'inputs/Rachelle/advanceAndRetreateProfil.skl'
#extractor.plotadvanceAndRetreate(fileName)

fileName = 'inputs/Rachelle/expending and condencing.skl'
extractor.plotExpendingCondencing(fileName)
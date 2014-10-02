import LabanUtils.informationGain as ig
import LabanUtils.util as labanUtil
import LabanUtils.combinationsParser as cp

def createDiagram(source, quality):
    ds, featuresNames = labanUtil.getPybrainDataSet(source) 
    X, Y = labanUtil.fromDStoXY(ds)
    qualities, combinations = cp.getCombinations()
    y = Y[qualities.index(quality)]
    fileName = source+quality
    ig.createDiagram(X, y, featuresNames, fileName)

quality = 'Strong'  
createDiagram('Rachelle', quality)  
createDiagram('Karen', quality)  
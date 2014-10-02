import LabanUtils.util as labanUtil
import LabanUtils.informationGain as ig
import utils.utils as utils
import matplotlib.pyplot as plt
import LabanUtils.combinationsParser as cp

CMAs = ['Rachelle', 'Karen']
trainSource = CMAs[0]
testSource = CMAs[1]
tstdata, featuresNames = labanUtil.getPybrainDataSet(testSource)  
print 'Data was read'
X2, Y2 = labanUtil.fromDStoXY(tstdata)
y=Y2[0]
igs, ps = ig.recursiveRanking(X2, y)
print igs
print max(igs)
"""
trndata, featuresNames = labanUtil.getPybrainDataSet(trainSource) 
X1, Y1 = labanUtil.fromDStoXY(trndata)
cors = []
for y1, y2 in zip(Y1, Y2):
    im1 = ig.infoGain(X1, y1)
    print im1
    ind = [i for i, e in enumerate(im1) if e != 0]
    print ind
    im2 = ig.infoGain(X2, y2)
    print im2
    ind = [i for i, e in enumerate(im2) if e != 0]
    print ind
    cor = utils.corr(im1, im2)
    print cor
    cors.append(cor)

qualities, combinations = cp.getCombinations()   
fig, ax = plt.subplots()
ax.bar(range(len(qualities)), cors)
ax.set_xticklabels(qualities)
plt.show()
"""
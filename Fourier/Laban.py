import utils.angleExtraction as ae
import matplotlib.pyplot as plt



#fileName = 'inputs/Rachelle/spreadindAndClosing.skl'
fileName = 'inputs/Rachelle/expending and condencing.skl'
f = open(fileName, 'r')
headers = f.readline().split()
numOfJoints = (len(headers)-2)/4
jointsIndices = [2+4*index for index in range(numOfJoints)]
input = []
input2 = []
for line in f:
    lineInFloats=[float(v) for v in line.split()]
    input.append(ae.calcDisFromIndices(lineInFloats, headers.index('HipCenter_X'), \
        headers.index('WristRight_X')))
    #input.append(ae.calcAverageJointDistanceFromCenter(lineInFloats, jointsIndices))
    #input.append(ae.calcAverageDistanceOfIndicesFromLine(lineInFloats, \
                #jointsIndices, headers.index('HipCenter_X'), headers.index('ShoulderCenter_X')))
plt.plot(input)
#plt.figure()
plt.show()    
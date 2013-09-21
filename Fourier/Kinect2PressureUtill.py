from jointsMap import ancestorMap, Joints


def getAnccestorRelativePos(splited):
    input = []
    for i in range(len(splited)):
        try:
            anc = ancestorMap[i]
            relativePos = float(splited[i]) - float(splited[anc])  
            input.append(relativePos)
        except:
            continue
    return input

filePath = 'asc_gyro_l.skl'
f = open(filePath, 'r')
headers = f.readline().split()
numOfFeatures = len(ancestorMap)
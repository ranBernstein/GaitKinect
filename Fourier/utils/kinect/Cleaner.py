import matplotlib.pyplot as plt
from jointsMap import Joints, ancestorMap


def plotJointCentered(file, joint, plot=False):
    f = open(file, 'r')
    headers = f.readline()
    time = []
    absJoints = []
    relJoints = []
    for line in f:
        splited = line.split()
        absPos = float(splited[joint])
        absJoints.append(absPos)
        centerPos = float(splited[ancestorMap[joint]])
        relPos = absPos - centerPos;
        relJoints.append(relPos);
        time.append(int(splited[Joints.timestamp]))
    if(plot):
        plt.figure()
        plt.scatter(time, absJoints)
        plt.figure()
        plt.scatter(time, relJoints)
    return time, relJoints
     

def plotJointCenteredPeriodicaly(file, joint):
    fourierValue = open(file, 'r')
    headers = fourierValue.readline()
    time = []
    periods = []
    lastTimeStamp = 0
    lastRelPos = 0
    firstIter = True
    # each line is a time stamp
    for line in fourierValue:
        splited = line.split()
        newTimeStamp = int(splited[Joints.timestamp])
        absPos = float(splited[joint])
        centerPos = float(splited[ancestorMap[joint]]) #float(splited[joint%4])
        relPos = absPos - centerPos;
        #if(not firstIter and abs(lastRelPos - relPos) > 0.15):
        #    continue
        #lastRelPos = relPos
        if(len(periods) > 0):
            period = periods[-1];
        if newTimeStamp - lastTimeStamp > 100 :
            periods.append([]);
            period = periods[-1]; 
        lastTimeStamp = newTimeStamp
        period.append((newTimeStamp, relPos));
        firstIter = False
    longPeriods=[];
    for period in periods:
        if(len(period) < 50):
            continue
        longPeriods.append(period)
    return longPeriods

def cleanPeriodsBias(periods): 
    cleanPeriods=[];
    for period in periods:
        cleanPeriod =cleanSeriesBias(period)
        cleanPeriods.append(cleanPeriod)
    return cleanPeriods

def cleanSeriesBias(period): 
    bias = sum(period)/len(period)
    cleanPeriod = []
    for sample in period:
        cleanPeriod.append(sample - bias)
    return cleanPeriod

def getMeanList(listOflists):
    roatetedListOfList = list(zip(*listOflists))#roatate
    meanList = []
    for roatetedList in roatetedListOfList:
        meanList.append(sum(roatetedList)/len(roatetedList))
    return meanList

def getMaxLenOfLists(lists):
    max = 0
    for list in lists:
        if len(list) > max :
            max = len(list)
    return max

def accumulateList(list):
    accumulated=[]
    sum = 0
    for e in list:
        sum += e
        accumulated.append(sum)
    return accumulated
import matplotlib.pyplot as plt
import utils.kinect.angleExtraction as ae
import algorithm.stitching as st
import numpy as np
import algorithm.partitionizing as part
f = open('myVicon/Yoni dyn 01.trc', 'r')
l = []
i=0
headers = []
for line in f:
    splited = line.split()
    if i==3:
        headers = splited
        t=[]
        for h in headers:
            s = h.split(':')
            if len(s)>1:
                for j in range(3):
                    t.append(s[1]+str(j))
            else:
                t.append(h)
        headers = t
    i+=1
    if i <=4 :
        continue
    res = ae.getAngleByColumns(splited, headers, 'LowBack0','Lhip0', 'Lknee0')#, 'Rankle0', 'Rfoot0')
    l.append(res)
    #print splited[46]
    #l.append(splited[headers.index('Rankle')])



i=0
time=[]
angles=[]
while i<len(l):
    while i<len(l) and l[i] != '' and l[i]!=None:
        time.append(i)
        angles.append(l[i])
        i+=1
    #if len(ts) >0:
        #plt.plot(ts,vs)
    i+=1
plt.plot(time, angles)
minimalCluster=20
fracs = []
lastT = time[0]
currTime = []
currAngles =[]
anglesSplited = []
for t, a in zip(time, angles):
    if np.abs(lastT - t) < 5:
        currTime.append(t)
        currAngles.append(a)
    else:
        if len(currAngles)>100:
            marginSize = int(len(currTime)*0.1)
            currAngles = currAngles[marginSize:-marginSize]
            #fracs.append((currTime, currAngles))
            anglesSplited.append(currAngles)
            currTime = [t]
            currAngles = [a]
    lastT = t
#fracs = ke.clusterByTime(time, angles, False, minimalCluster)
#cleanedParts, kuku = ke.cleanFracs(fracs, False)
st.plotParts(anglesSplited)
periods =[]
strides = []
stances = []
swings = []
for cluster in anglesSplited:
    maximaOrder=27
    clusteringGranularity=0.5
    breaked = part.breakToPeriods(cluster,maximaOrder, clusteringGranularity)
    for cycle in breaked:
        if len(cycle)>80 and len(cycle)<180:
            #periods.append(cycle)
            strides.append(cycle)
            min = np.argmin(cycle)
            stances.append(cycle[:min])
            swings.append(cycle[min:])

part.plotStas(strides, 'Strides')
part.plotStas(stances, 'stances')
part.plotStas(swings, 'swings')
plt.show()















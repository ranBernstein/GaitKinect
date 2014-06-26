import matplotlib.pyplot as plt
import utils.kinect.angleExtraction as ae

#f = open('myVicon/Ido dyn 01.csv', 'r')
f = open('myVicon/Ran dyn 03.csv', 'r')
#f = open('myVicon/Yoni dyn 01.csv', 'r')
l = []
i=0
headers = []
for line in f:
    splited = line.split(',')
    if i==9:
        headers = splited
    i+=1
    if i <=11 :
        continue
    res = ae.getAngleByColumns(splited, headers,'LowBack', 'Lhip', 'Lknee')
    l.append(res)
    #print splited[46]
    #l.append(splited[headers.index('Rankle')])
print headers.index('Rankle')
print l



i=0
while i<len(l):
    ts=[]
    vs=[]
    while i<len(l) and l[i] != '':
        ts.append(i)
        vs.append(l[i])
        i+=1
    if len(ts) >0:
        plt.plot(ts,vs)
    i+=1
plt.show()
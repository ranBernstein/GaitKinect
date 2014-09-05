import matplotlib.pyplot as plt 
fileName = 'results/1000WD0_8SP0_5.out'
f=open(fileName, 'r')
trainErrors=[]
testErrors=[]
for line in f:
    if 'epoch:' in line:
        line=line.split()
        trainErrors.append(float(line[4][:-1]))
        testErrors.append(float(line[7][:-1]))

fig = plt.figure()
ax = fig.add_subplot(111)
ax.plot(trainErrors, label='Train')
ax.plot(testErrors, label='Test')
ax.annotate('20% Error', xy=(800, 20), xytext=(750, 30),
            arrowprops=dict(facecolor='black', shrink=0.05),)
plt.xlabel('Convergence over epoches')
plt.ylabel('Error rate in percentage')
plt.legend().draggable()
plt.show()
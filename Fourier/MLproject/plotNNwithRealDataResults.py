import matplotlib.pyplot as plt
f = open('results/1000WD0_8SP0_5.out')
train=[]
test=[]
for line in f:
    if 'epoch:' in line:
        train.append(float(line.split()[4][:-1]))
        test.append(float(line.split()[7][:-1]))

plt.plot(train, label='train')
plt.plot(test, label='test')
plt.xlabel('epochs')
plt.ylabel('Error in percents')
plt.title('Convergence over epochs')
plt.legend().draggable()
plt.show()
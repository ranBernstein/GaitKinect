import matplotlib.pyplot as plt
precenteges = [20, 30, 40, 50, 60, 70, 80, 85, 90, 97, 98]
v10 = [38.0/56, 34.0/49, 33.0/42, 29.0/35, 25.0/28, 18.0/21, 12.0/14, 9.0/10, 1, 1, 1]
v50 = [31.0/56, 28.0/49, 36.0/42, 31.0/35, 25.0/28, 19.0/21, 12.0/14, 10.0/10, 7/7 , 2/2, 1]
v1178 = [25.0/56, 19.0/49, 35.0/42, 30.0/35, 26.0/28, 19.0/21, 12.0/14, 10.0/10, 7/7, 1, 1]
print len(v10), len(v50), len(v1178), len(precenteges)

"""
plt.title('Accuracy as function of train set proportion of different number of features')
plt.xlabel('Percentage of the train set from the whole data')
plt.ylabel('Success rate in test set')
plt.plot(precenteges, v10, 'r-', label='10 features')
plt.plot(precenteges, v50, 'r--', label='50 features')
plt.plot(precenteges, v1178, 'r:', label='1178 features')
plt.legend().draggable()
plt.ylim((0, 1.5))
plt.show()
"""

algos = ['SVM', 'Multilayer perceptron', 'Naive Bayse', 'RBF Network', 'Functional trees', 'Best-first tree' ]
performence = [23.0/35, 20.0/35, 14.0/35, 27.0/35, 24.0/35, 15.0/35]
r = range(1, len(performence)+1)
plt.title('Accuracy of different algorithms with train set of 50%')
#plt.xlabel('Algorithm')
plt.ylabel('Success rate in test set')
plt.bar(r, performence, align='center')
plt.xticks(r, algos)
plt.show()
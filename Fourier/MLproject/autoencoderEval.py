import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
import numpy as np
sizes = [5, 10, 20, 50, 75, 100, 150, 175, 200,
          225, 250, 300, 350, 400, 500, 600]
accuracy = [5, 18, 18, 19, 21, 24, 20, 22, 19, 19, 24, 20, 25, 21, 25, 23]
reg = LinearRegression()
a = np.reshape(np.array(sizes), (len(sizes), 1))
reg.fit(a, accuracy)
print reg.predict(a)

plt.plot(sizes, accuracy, label='Original results')
plt.plot(sizes, reg.predict(a), label='Linear regression approximation')
plt.xlabel('Size of hidden layer')
plt.ylabel('Number of correct samples out of 35')
plt.legend().draggable()
plt.show()
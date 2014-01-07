import matplotlib.pyplot as plt
import matplotlib.cm as cm
import mlpy

def alignByFirst(vec1, vec2, compareFunc):
    if(len(vec1) != len(vec2)):
        raise 'not the same length'
    bestGrade = 0
    bestVec = None
    for shift in xrange(vec1):
        newVec2 = vec2[-shift:] + vec2[:-shift]
        grade = compareFunc(vec1, newVec2)
        if(grade > bestGrade):
            bestGrade = grade
            bestVec = newVec2
    return vec1, bestVec

x = [0,0,0,0,1,1,2,2,3,2,1,1,0,0,0,0]
y = [0,0,1,1,2,2,3,3,3,3,2,2,1,1,0,0]
dist, cost, path = mlpy.dtw_std(x, y, dist_only=False)
print(dist)
fig = plt.figure(1)
ax = fig.add_subplot(111)
plot1 = plt.imshow(cost.T, origin='lower', interpolation='nearest')
plot2 = plt.plot(path[0], path[1], 'w')
xlim = ax.set_xlim((-0.5, cost.shape[0]-0.5))
ylim = ax.set_ylim((-0.5, cost.shape[1]-0.5))
plt.show()
import Laban.algorithm.generalExtractor as ge
import numpy as np
#from sklearn.decomposition import PCA
import matplotlib.pyplot as plt 
from matplotlib.mlab import PCA
import mlpy 
#coupels = [['anger', 'happy']]
coupels = [['anger', 'fear'], ['anger', 'happy'], ['anger', 'sad'], ['happy', 'fear'], ['sad', 'fear'], ['sad', 'happy']]
#moods = ['anger', 'fear']#, 'happy', 'sad', 'neutral']
#data2 = [[],[]]
for couple in coupels:
    i=0
    data = []
    for mood in couple:
        for typeNum in range(1,21):
            for take in range(1,10):
                fileName = '../inputs/Rachelle/v2/recordingsByMood/'+mood+'/'+\
                str(typeNum)+'_'+str(take)+'.skl'
                try:
                    vec = ge.getFeatureVec(fileName, ['WristRight_X', 'WristLeft_X'])
                except IOError:
                    continue
                data.append(vec)
                #data2[couple.index(mood)].append(vec)
                i+=couple.index(mood)
    a= np.array(data)
    print a.shape
    results = PCA(a)
    print results.fracs
    x = []
    y = []
    for item in results.Y[:-i]:
        x.append(item[0])
        y.append(item[1])
    plt.figure()
    plt.scatter(x, y, c='b')
    x = []
    y = []
    for item in results.Y[-i:]:
        x.append(item[0])
        y.append(item[1])
    plt.scatter(x, y, c='r')
    plt.title(str(couple))
"""
    class1=np.array(data[0])
    class2=np.array(data[1])
    mean1=np.mean(class1, axis=0)
    mean2=np.mean(class2, axis=0)
    
    #calculate variance within class
    Sw=np.dot((class1-mean1).T, (class1-mean1))+np.dot((class2-mean2).T, (class2-mean2))
    
    #calculate weights which maximize linear separation
    w=np.dot(np.linalg.inv(Sw), (mean2-mean1))
    
    print "vector of max weights", w
    #projection of classes on 1D space
    plt.plot(np.dot(class1, w), [0]*class1.shape[0], "bo", label=couple[0])
    plt.plot(np.dot(class2, w), [0]*class2.shape[0], "go", label=couple[1])
    plt.legend()
plt.show()
"""
plt.show()









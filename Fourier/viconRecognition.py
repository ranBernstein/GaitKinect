from amcParser import getAMCperiod
from periodAnalysisUtils import alignByMax
import matplotlib.pyplot as plt

file = 'AMCs/subjects/16/3.amc'
joint = 'rtibia'
input = getAMCperiod(joint, file)
input = alignByMax(input)
plt.plot(range(len(input)), input)
plt.xlabel('Time (in frames)')
plt.ylabel(joint + ' angle')
plt.title(file)
plt.show()
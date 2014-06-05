import sys
from PyQt4 import QtGui

from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QTAgg as NavigationToolbar
import matplotlib.pyplot as plt
import renderSkeleton as render
import random
import pandas as pd

class Window(QtGui.QDialog):
    def __init__(self, parent=None):
        super(Window, self).__init__(parent)

        # a figure instance to plot on
        self.figure = plt.figure()

        # this is the Canvas Widget that displays the `figure`
        # it takes the `figure` instance as a parameter to __init__
        self.canvas = FigureCanvas(self.figure)

        # this is the Navigation widget
        # it takes the Canvas widget and a parent
        self.toolbar = NavigationToolbar(self.canvas, self)

        # Just some button connected to `plot` method
        self.button = QtGui.QPushButton('Plot')
        self.button.clicked.connect(self.plot)

        # set the layout
        self.layout = QtGui.QVBoxLayout()
        self.layout.addWidget(self.toolbar)
        self.layout.addWidget(self.canvas)
        self.layout.addWidget(self.button)
        #self.setLayout(self.layout)
        
        data = [random.random() for i in range(10)]

        # create an axis
        ax = self.figure.add_subplot(111)

        # discards the old graph
        #ax.hold(False)

        # plot data
        ax.plot(data, '*-')

        # refresh canvas
        self.addSkeletonWindow()
        self.canvas.draw()
        
    def addSkeletonWindow(self):
        t_start = 1917 # start frame
        t_end = 2130 # end frame
        
        data = pd.read_csv('../inputs/Smart-first_phase_NaN-zeros.csv') # only coordinate data
        df = data.loc[t_start:t_end,'Shoulder_left_x':'Ankle_right_z']
        data = df.values.tolist()
        
        def chunks(l, n):
            return [l[i:i+n] for i in range(0, len(l), n)]
                
        newData = []
        for line in data:
            newData.append(chunks(line, 3))
        figure = render.renderSkeleton(newData)
        layout = QtGui.QVBoxLayout()
        canvas = FigureCanvas(figure)
        toolbar = NavigationToolbar(canvas, self)
        self.layout.addWidget(toolbar)
        self.layout.addWidget(canvas)
        button = QtGui.QPushButton('Plot')
        self.layout.addWidget(button)
        self.setLayout(self.layout)
        canvas.draw()
        plt.show()
        
    def plot(self):
        ''' plot some random stuff '''
        # random data
        data = [random.random() for i in range(10)]

        # create an axis
        ax = self.figure.add_subplot(111)

        # discards the old graph
        #ax.hold(False)

        # plot data
        ax.plot(data, '*-')

        # refresh canvas
        self.canvas.draw()

if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)

    main = Window()
    main.show()

    sys.exit(app.exec_())
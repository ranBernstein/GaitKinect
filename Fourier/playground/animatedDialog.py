from mpl_toolkits.mplot3d import Axes3D    # @UnusedImport
from PySide import QtGui, QtCore

import matplotlib
import matplotlib.animation as animation
import sys
# specify the use of PySide
matplotlib.rcParams['backend.qt4'] = "PySide"

# import the figure canvas for interfacing with the backend
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg \
                                                            as FigureCanvas
from matplotlib.figure import Figure

import numpy as np
from math import pi, cos, sin


class Ui_MainWindow(object):
    def setupUi(self, MainWindow, direction, maxRadius):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 500)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayout = QtGui.QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.pushButton = QtGui.QPushButton(self.centralwidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum,
                                       QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
                            self.pushButton.sizePolicy().hasHeightForWidth())
        self.pushButton.setSizePolicy(sizePolicy)
        self.pushButton.setMaximumSize(QtCore.QSize(150, 16777215))
        self.pushButton.setObjectName("pushButton")
        self.pushButton.setText("Change Direction")
        self.horizontalLayout.addWidget(self.pushButton)
        self.frame = QtGui.QFrame(self.centralwidget)
        self.frame.setFrameShape(QtGui.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtGui.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.gridLayout = QtGui.QGridLayout(self.frame)
        self.gridLayout.setObjectName("gridLayout")
        self.horizontalLayout.addWidget(self.frame)
        # ------
        self.mplWidget = MplWidget(None, direction, maxRadius)
        self.gridLayout.addWidget(self.mplWidget)
        # ------
        MainWindow.setCentralWidget(self.centralwidget)

        QtCore.QMetaObject.connectSlotsByName(MainWindow)


class MainWindow(QtGui.QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.ui = Ui_MainWindow()
        self.direction = 'up'
        self.maxRadius = 0.3
        self.ui.setupUi(self, self.direction, self.maxRadius)
        self.ui.pushButton.clicked.connect(self.changeStuff)
        self.animation = self.ui.mplWidget.animate()

    def changeStuff(self):
        self.ui.mplWidget.close_event()  # mpl clean up
        self.ui.mplWidget.deleteLater()  # QT cleanup
        self.ui.gridLayout.removeWidget(self.ui.mplWidget)

        dirs = {'up': 'down', 'down': 'up'}
        rads = {0.3: 1, 1: 0.3}
        self.direction = dirs[self.direction]
        self.maxRadius = rads[self.maxRadius]
        self.ui.mplWidget = MplWidget(self.ui.frame, self.direction,
                                      self.maxRadius)
        self.ui.gridLayout.addWidget(self.ui.mplWidget)
        self.animation = self.ui.mplWidget.animate()
        print self.ui.frame.children()
        print 'finished change stuff'


class MplWidget(FigureCanvas):
    def __init__(self, parent=None, direction='up', maxRadius=0.3):
        self.figure = Figure()
        super(MplWidget, self).__init__(self.figure)
        self.setParent(parent)
        self.axes = self.figure.add_subplot(111, projection='3d')
        self.axes.set_xlabel("x label")
        self.axes.set_ylabel("y label")
        self.axes.set_zlabel("z label")
        self.axes.set_xlim3d([-1, 1])
        self.axes.set_ylim3d([-1, 1])
        self.axes.set_zlim3d([-1, 1])
        self.axes.set_aspect('equal')
        if direction == 'up':
            self.c = 1
        elif direction == 'down':
            self.c = -1
        else:
            self.c = 1
        self.maxRadius = maxRadius
        self.frames = 50
        self.plot_handle = self.func_plot(self.frames)

    def func_plot(self, z):
        z /= float(self.frames) * self.c
        theta = np.arange(0, 2 * pi + pi / 50, pi / 50)
        xdata = self.maxRadius * z * np.array([cos(q) for q in theta])
        ydata = self.maxRadius * z * np.array([sin(q) for q in theta])
        zdata = z * np.ones(np.shape(xdata))
        if not hasattr(self, 'plot_handle'):
            plot_handle = self.axes.plot(xdata, ydata, zdata)[0]
        else:
            plot_handle = self.plot_handle
        plot_handle.set_data(xdata, ydata)
        plot_handle.set_3d_properties(zdata)
        return plot_handle

    def animate(self):
        return animation.FuncAnimation(
                    fig=self.figure, func=self.func_plot, frames=self.frames,
                    interval=1000.0 / self.frames, blit=False)

if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    mw = MainWindow()
    mw.show()
    sys.exit(app.exec_())
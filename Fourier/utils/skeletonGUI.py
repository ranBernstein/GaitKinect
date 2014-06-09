from mpl_toolkits.mplot3d import Axes3D    # @UnusedImport
from PySide import QtGui, QtCore
import pandas as pd
from matplotlib import pyplot as plt
from PyQt4.QtCore import pyqtSlot,SIGNAL,SLOT
#from PyQt4.QtCore.Qt.Unchecked import Unchecked
import PyQt4.QtCore
import matplotlib
import matplotlib.animation as animation
import sys
from  utils.kinect import jointsMap 
import os
# specify the use of PySide
matplotlib.rcParams['backend.qt4'] = "PySide"

# import the figure canvas for interfacing with the backend
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg \
                                                as FigureCanvas
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QTAgg \
                                                 as NavigationToolbar
                                                           
from matplotlib.figure import Figure

import numpy as np
from math import pi, cos, sin


class Ui_MainWindow(object):
    def __init__(self, mainWindow):
        self.mainWindow = mainWindow
        self.showSticks=False
        self.showTrajectories=False
        self.rotate=False
        self.start = 0
        
    def setupUi(self, MainWindow, direction, maxRadius):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 500)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.mainLayout = QtGui.QVBoxLayout(self.centralwidget)       
        
        #frame
        self.frame = QtGui.QFrame(self.centralwidget)
        self.frame.setFrameShape(QtGui.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtGui.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.mainLayout.addWidget(self.frame)
        self.gridLayout = QtGui.QGridLayout(self.frame)
        self.gridLayout.setSpacing(10)
        
        #slider
        sliderEdit = QtGui.QLineEdit()
        sliderEdit.setEnabled(False)
        sliderEdit.setFixedWidth(40)
        self.slider = QtGui.QSlider(self.centralwidget)
        self.changedProgrammatically = False
        def changePos():
            currFarme = self.slider.value()
            sliderEdit.setText(str(currFarme))
            if not self.changedProgrammatically:
                self.start = currFarme
                self.skeletonPlot.init(self.start)    
        self.slider.valueChanged.connect(changePos)
        self.gridLayout.addWidget(sliderEdit, 0,0)
        self.gridLayout.addWidget(self.slider, 1,0)
        
        #skeleton options
        self.showSticksCheckbox = QtGui.QCheckBox("Show sticks", MainWindow)
        QtCore.QObject.connect(self.showSticksCheckbox,\
             SIGNAL("stateChanged(int)"),self.mainWindow,SLOT("showSticksSlot(int)"))
        
        self.showTrajectoriesCheckbox = QtGui.QCheckBox("Show trajectories", MainWindow)
        QtCore.QObject.connect(self.showTrajectoriesCheckbox,\
             SIGNAL("stateChanged(int)"),self.mainWindow,SLOT("showTrajectoriesSlot(int)"))
        
        self.rotateCheckbox = QtGui.QCheckBox("Rotate", MainWindow)
        QtCore.QObject.connect(self.rotateCheckbox,\
             SIGNAL("stateChanged(int)"),self.mainWindow,SLOT("rotateSlot(int)"))
        
        self.renderOptionsLayout = QtGui.QVBoxLayout(self.centralwidget)
        self.renderOptionsLayout.setObjectName("renderOptionsLayout")
        self.renderOptionsLayout.addWidget(self.showSticksCheckbox)
        self.renderOptionsLayout.addWidget(self.rotateCheckbox)
        self.renderOptionsLayout.addWidget(self.showTrajectoriesCheckbox)
        self.showTrajectoriesCheckbox.setFixedWidth(120)
        self.gridLayout.addLayout(self.renderOptionsLayout, 1, 1)
        
        #skeletonPlot
        openFile = QtGui.QPushButton(self.centralwidget)
        openFile.setText("Choose Input")
        openFile.setFixedWidth(120)
        self.fileEdit = QtGui.QLineEdit()
        def selectFile():
            res= unicode(QtGui.QFileDialog.getOpenFileName()[0])
            self.fileEdit.setText(res)
            self.mainWindow.animation = self.skeletonPlot.animate(res)
        openFile.clicked.connect(selectFile)
        self.gridLayout.addWidget(openFile, 0,2)
        self.gridLayout.addWidget(self.fileEdit, 0, 3,1,2)
        self.skeletonPlot = SkeletonPlot(self.mainWindow, direction, maxRadius)
        self.gridLayout.addWidget(self.skeletonPlot,1,2,1,3)
        toolbar = NavigationToolbar(self.skeletonPlot, self.mainWindow)
        self.gridLayout.addWidget(toolbar,2,2,1,3)
        
        #analysisPlot
        chooseAnalysis = QtGui.QPushButton(self.centralwidget)
        chooseAnalysis.setText("Choose Analysis")
        chooseAnalysis.setFixedWidth(120)
        analysisEdit = QtGui.QLineEdit()
        def selectAnalysis():
            res= QtGui.QFileDialog.getOpenFileName()[0]
            analysisEdit.setText(res)
            os.system("script2.py 1")
        chooseAnalysis.clicked.connect(selectAnalysis)
        analysisFig = plt.figure()
        analysisFig.patch.set_facecolor('white')
        self.analysisPlot = FigureCanvas(analysisFig)
        self.analysisSubPlot = analysisFig.add_subplot(1,1,1)
        #self.analysisSubPlot.plot([1,2,3,4,5,4,3,6,7])
        self.analysisPlot.draw()
        toolbar = NavigationToolbar(self.analysisPlot, self.mainWindow)
        MainWindow.setCentralWidget(self.centralwidget)
        self.gridLayout.addWidget(chooseAnalysis,0,5)
        self.gridLayout.addWidget(analysisEdit,0,6,1,2)
        self.gridLayout.addWidget(self.analysisPlot, 1,5,1,3)
        self.gridLayout.addWidget(toolbar,2,5,1,3)

        QtCore.QMetaObject.connectSlotsByName(MainWindow)


class MainWindow(QtGui.QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.ui = Ui_MainWindow(self)
        self.direction = 'up'
        self.maxRadius = 0.3
        self.ui.setupUi(self, self.direction, self.maxRadius)
        #self.ui.pushButton.clicked.connect(self.openFile)
        #self.animation = self.ui.skeletonPlot.animate()
          
    @pyqtSlot(int)
    def showSticksSlot(self,state):
        self.ui.skeletonPlot.showSticks = self.ui.showSticksCheckbox.isChecked()
        self.ui.skeletonPlot.init(self.ui.start)
        
    @pyqtSlot(int)
    def showTrajectoriesSlot(self,state):
        fig = self.ui.skeletonPlot
        fig.showTrajectory = self.ui.showTrajectoriesCheckbox.isChecked()
        #fig.lines = sum([fig.ax.plot([], [], [], '-', c=c) for c in fig.colors], [])
        self.ui.skeletonPlot.init(self.ui.start)
        
    @pyqtSlot(int)
    def rotateSlot(self,state):
        self.ui.skeletonPlot.rotate = self.ui.rotateCheckbox.isChecked()

class SkeletonPlot(FigureCanvas):
    def __init__(self, mainWindow, direction='up', maxRadius=0.3):
        
        self.showSticks, self.rotate, self.showTrajectory = False, False, False
        self.hirarchy=None
        self.mainWindow = mainWindow
        self.figure = Figure()
        self.figure.patch.set_facecolor('white')
        super(SkeletonPlot, self).__init__(self.figure)
        self.setParent(mainWindow)
        
    def init(self, start=0):
        self.start = start
        for line, pt in zip(self.lines, self.pts):
            # trajectory lines
            line.set_data([], [])
            line.set_3d_properties([])
            # points
            pt.set_data([], [])
            pt.set_3d_properties([])
        return self.lines + self.pts + self.stick_lines
    def animate(self, fileName):
        f= open(fileName, 'r')
        headers=f.readline().split()
        self.hirarchy = jointsMap.getHirarchy(headers)
        joints = jointsMap.getJoints(headers)
        jointsNum = len(joints)
        fileLength=0
        for line in f:
            fileLength+=1
        self.mainWindow.ui.slider.setRange(0, fileLength)
        x_t = np.zeros(shape=(jointsNum,fileLength,3)) # empty animation array (3D)
        f= open(fileName, 'r')
        f.readline()
        for i,line in enumerate(f):
            lineF=[float(v) for v in line.split()]
            for j, joint in enumerate(joints):
                x_t[j,i,:] = [lineF[headers.index(joint+'_X')],lineF[headers.index(joint+'_Y')],\
                              lineF[headers.index(joint+'_Z')],]
        
        fig = self.figure
        self.ax = fig.add_axes([0, 0, 1, 1], projection='3d')
        self.ax.axis('on')
        #Adjust data to matplotlib axes
        x_t = x_t[:, :, [2, 0, 1]]
        self.ax.set_xlabel("Z axe")
        self.ax.set_ylabel("X axe")
        self.ax.set_zlabel("Y axe")
        
        # choose a different color for each trajectory
        self.colors = plt.cm.jet(np.linspace(0, 1, jointsNum))
        # set up trajectory lines
        self.lines = sum([self.ax.plot([], [], [], '-', c=c) for c in self.colors], [])
        # set up points
        self.pts = sum([self.ax.plot([], [], [], 'o', c=c) for c in self.colors], [])
        # set up lines which create the stick figures
        
        self.stick_lines = [self.ax.plot([], [], [], 'k-')[0] for _ in self.hirarchy]
        
        # prepare the axes limits
        self.ax.set_xlim((np.min(x_t[:,:,0]),np.max(x_t[:,:,0])))
        self.ax.set_ylim((np.min(x_t[:,:,1]),np.max(x_t[:,:,1]))) # note usage of z coordinate
        self.ax.set_zlim((np.min(x_t[:,:,2]),np.max(x_t[:,:,2]))) # note usage of y coordinate
        # set point-of-view: specified by (altitude degrees, azimuth degrees)
        self.ax.view_init(30, 0)
        self.ax.set_aspect('auto')
        def myAnimate(i):
            # we'll step two time-steps per frame.  This leads to nice results.
            #i = (5 * i) % x_t.shape[1]
            currValue = self.start + i
            self.mainWindow.ui.changedProgrammatically = True
            #if(i%10 == 0):
            self.mainWindow.ui.slider.setValue(currValue)
            self.mainWindow.ui.changedProgrammatically = False
            for line, pt, xi in zip(self.lines, self.pts, x_t):
                x, y, z = xi[self.start:currValue].T 
                pt.set_data(x[-1:], y[-1:])
                pt.set_3d_properties(z[-1:])
                
                # trajectory lines
                if self.showTrajectory:
                    line.set_data(x,y)
                    line.set_3d_properties(z)
                    
            if self.showSticks:
                if self.hirarchy is None:
                    QtGui.QMessageBox.information(self,"Can't complete command",\
                                                    'Hirarchy is missing')
                    self.showSticks = False
                    #self.parent.ui.showSticksCheckbox.setCheckState(QtCore.Qt.Unchecked)
                else:    
                    for stick_line, (sp, ep) in zip(self.stick_lines, self.hirarchy):
                        stick_line._verts3d = x_t[[sp,ep], i, :].T.tolist()
            else:
                for stick_line in self.stick_lines:
                    stick_line._verts3d = [[],[],[]]
                    
            if self.rotate:
                self.ax.view_init(30, i)
            fig.canvas.draw()
            return self.lines + self.pts + self.stick_lines
        return animation.FuncAnimation(
                    fig, myAnimate,init_func=self.init, interval=33, blit=True)

if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    mw = MainWindow()
    mw.show()
    sys.exit(app.exec_())
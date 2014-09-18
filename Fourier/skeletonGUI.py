from PyQt4 import QtGui, QtCore
import pandas as pd
from matplotlib import pyplot as plt
from PyQt4.QtCore import pyqtSlot,SIGNAL,SLOT
#from PyQt4.QtCore.Qt.Unchecked import Unchecked
from PyQt4.QtGui import QPixmap
import matplotlib
import matplotlib.animation as animation
from mplot3d import Axes3D    # @UnusedImport
import sys
from  utils.kinect import jointsMap 
import os
import importlib
from GUI.ClickableQLabel import ClickableQLabel
import GUI.analysisGUI as ag

# import the figure canvas for interfacing with the backend
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg \
                                                as FigureCanvas
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QTAgg \
                                                 as NavigationToolbar
                                                           
from matplotlib.figure import Figure

import numpy as np
from math import pi, cos, sin
from PyQt4.Qt import QLabel


class Ui_MainWindow(object):
    def __init__(self, mainWindow):
        self.mainWindow = mainWindow
        self.showSticks=False
        self.showTrajectories=False
        self.rotate=False
        self.start = 0
        self.syncSkeletonWithAnalysis = False
        self.skeletonFileLength = 0
        
    def selectFile(self):
        self.mainWindow.stop = True
        dlg = QtGui.QFileDialog(self.centralwidget)
        dlg.setDirectory('inputs/Rachelle')
        self.selectedFile= unicode(dlg.getOpenFileName())
        self.fileEdit.setText(self.selectedFile)
        if os.path.isfile(self.selectedFile):
            self.syncWithAnalysis.setChecked(False)
            self.analysisEditor.initCanvas()
        
        def syncWithSkelaton(event):
            if not self.syncSkeletonWithAnalysis:
                return
            self.updateCurrTime(event.xdata)
        self.analysisEditor.prepareAnalysisEditorBeforeSync(syncWithSkelaton)
        
    
    def updateCurrTime(self, currTime):
        self.changedProgrammatically = True
        self.mainWindow.currTime = currTime
        self.slider.setValue(currTime)
        if self.syncSkeletonWithAnalysis:
            self.analysisEditor.updateAnalysisTimeMarker()
                
    
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1000, 700)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.mainLayout = QtGui.QVBoxLayout(self.centralwidget)       
        self. analysisEditor = ag.AnalysisEditor(self)
        #frame
        self.frame = QtGui.QFrame(self.centralwidget)
        self.frame.setFrameShape(QtGui.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtGui.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.mainLayout.addWidget(self.frame)
        self.gridLayout = QtGui.QGridLayout(self.frame)
        self.gridLayout.setSpacing(0)        

        #skeleton options
        self.syncWithAnalysis = QtGui.QCheckBox("Sync marker", MainWindow)
        QtCore.QObject.connect(self.syncWithAnalysis,\
             SIGNAL("stateChanged(int)"),self.mainWindow,SLOT("syncWithAnalysis(int)"))
        
        self.showSticksCheckbox = QtGui.QCheckBox("Show sticks", MainWindow)
        QtCore.QObject.connect(self.showSticksCheckbox,\
             SIGNAL("stateChanged(int)"),self.mainWindow,SLOT("showSticksSlot(int)"))
        
        self.showTrajectoriesCheckbox = QtGui.QCheckBox("Show trajectories", MainWindow)
        QtCore.QObject.connect(self.showTrajectoriesCheckbox,\
             SIGNAL("stateChanged(int)"),self.mainWindow,SLOT("showTrajectoriesSlot(int)"))
        
        self.rotateCheckbox = QtGui.QCheckBox("Rotate", MainWindow)
        QtCore.QObject.connect(self.rotateCheckbox,\
             SIGNAL("stateChanged(int)"),self.mainWindow,SLOT("rotateSlot(int)"))
        
        renderOptionsLayout = QtGui.QVBoxLayout()
        renderOptionsLayout.setObjectName("renderOptionsLayout")
        renderOptionsLayout.addWidget(self.syncWithAnalysis)
        renderOptionsLayout.addWidget(self.showSticksCheckbox)
        renderOptionsLayout.addWidget(self.rotateCheckbox)
        renderOptionsLayout.addWidget(self.showTrajectoriesCheckbox)
        self.showTrajectoriesCheckbox.setFixedWidth(120)
        #self.gridLayout.addLayout(renderOptionsLayout, 3, 0)
        
        #play toolbar
        toolbarLayout = QtGui.QHBoxLayout()
        def createImageButton(path):
            label = ClickableQLabel()
            labelImage = QtGui.QImage(path)
            pp = QPixmap.fromImage(labelImage)
            scaledPixmap = pp.scaled(self.rotateCheckbox.size(), QtCore.Qt.KeepAspectRatio)
            label.setPixmap(scaledPixmap)
            def p():
                pass
            return label
        play = createImageButton('images/play.png')
        QtCore.QObject.connect(play, SIGNAL("clicked()"),self.mainWindow,SLOT("play()"))
        toolbarLayout.addWidget(play)
        
        pause = createImageButton('images/pause.png')
        QtCore.QObject.connect(pause, SIGNAL("clicked()"),self.mainWindow,SLOT("pause()"))
        toolbarLayout.addWidget(pause)
        
        stop = createImageButton('images/stop.png')
        QtCore.QObject.connect(stop, SIGNAL("clicked()"),self.mainWindow,SLOT("stop()"))
        toolbarLayout.addWidget(stop)
        self.speedSlider = QtGui.QSlider()
        self.speedSlider.setRange(1,60)
        edit = QtGui.QLineEdit()
        edit.setFixedWidth(30)
        def speedChanged():
            self.mainWindow.playingSpeed = self.speedSlider.value()
            edit.setText(str(self.speedSlider.value()))
            self.mainWindow.stop = True
            self.mainWindow.play()
        self.speedSlider.setValue(self.mainWindow.playingSpeed)
        edit.setText(str(self.speedSlider.value()))
        self.speedSlider.valueChanged.connect(speedChanged)
        
        def speedChangedFromEdit():
            speed = int(edit.text())
            self.mainWindow.playingSpeed = speed
            self.speedSlider.setValue(speed)
            self.mainWindow.stop = True
            self.mainWindow.play()
        
        edit.textChanged.connect(speedChangedFromEdit)
        #self.gridLayout.addLayout(toolbarLayout, 0,0)
        label = QLabel('Play speed\n in Fps:')
        playSpeedLayout =  QtGui.QVBoxLayout()
        playSpeedLayout.addLayout(toolbarLayout)
        playSpeedLayout.addWidget(label)
        playSpeedLayout.addWidget(edit)
        playSpeedLayout.addWidget(self.speedSlider)
        playSpeedLayout.addLayout(renderOptionsLayout)
        label.setFixedWidth(60)
        self.gridLayout.addLayout(playSpeedLayout, 0, 0,3,1)
        #self.gridLayout.setRowStretch(0, 0)
        
        
        #skeletonPlot
        openFile = QtGui.QPushButton(self.centralwidget)
        openFile.setText("Choose Input")
        openFile.setFixedWidth(100)
        self.fileEdit = QtGui.QLineEdit()
        openFile.clicked.connect(self.selectFile)
        self.gridLayout.addWidget(openFile, 0,1)
        self.gridLayout.addWidget(self.fileEdit, 0, 2)
        self.skeletonPlot = SkeletonPlot(self.mainWindow)
        self.gridLayout.addWidget(self.skeletonPlot,1,1,1,2)
        toolbar = NavigationToolbar(self.skeletonPlot, self.mainWindow)
        self.gridLayout.addWidget(toolbar,2,1,1,2)
        
        
        self.gridLayout.addWidget(self.analysisEditor.chooseAnalysis, 0,3)
        self.gridLayout.addWidget(self.analysisEditor.lineEdit, 0,4)
        self.gridLayout.addWidget(self.analysisEditor.analysisCanvas, 1,3,1,2)
        self.gridLayout.addWidget(self.analysisEditor.toolbar, 2,3,1,2)
        self.gridLayout.addLayout(self.analysisEditor.analysisOperationsLayout,1,5)
        self.gridLayout.setRowMinimumHeight(1,700)
        #slider
        sliderEdit = QtGui.QLineEdit()
        sliderEdit.setEnabled(False)
        sliderEdit.setFixedWidth(40)
        self.slider = QtGui.QSlider(QtCore.Qt.Horizontal)
        self.changedProgrammatically = False
        def changePos():
            currFrame = self.slider.value()
            sliderEdit.setText(str(currFrame))
            if not self.changedProgrammatically:
                self.start = currFrame
                self.skeletonPlot.init(self.start)    
            self.changedProgrammatically=False
        self.slider.valueChanged.connect(changePos)
        self.gridLayout.addWidget(self.slider, 3, 0, 1,5)
        self.gridLayout.addWidget(sliderEdit, 3, 5)
        #self.gridLayout.setRowStretch(3, 0)
        MainWindow.setCentralWidget(self.centralwidget)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        
class MainWindow(QtGui.QMainWindow):
    def __init__(self, parent=None):
        self.pause = False
        self.stop = True
        self.currTime = 0
        self.start = 0
        self.animation = None
        self.playingSpeed = 30
        super(MainWindow, self).__init__(parent)
        self.ui = Ui_MainWindow(self)
        self.ui.setupUi(self)
    
    @pyqtSlot()
    def play(self):
        self.pause = False
        if os.path.isfile(self.ui.selectedFile):
            if self.stop == True:
                if not self.animation is None:
                    self.animation._stop()
                self.animation = self.ui.skeletonPlot.animate(self.ui.selectedFile)
        self.stop = False
        self.pause = False
    
    @pyqtSlot()
    def pause(self):
        self.pause = True
    
    @pyqtSlot()
    def stop(self):
        self.stop = True
        self.pause = False
        self.ui.skeletonPlot.init()     
    
    @pyqtSlot(int)
    def syncWithAnalysis(self,state):
        if state:
            self.ui.syncSkeletonWithAnalysis = True
            self.ui.analysisEditor.initTimeMarker()
        else:
            self.ui.analysisEditor.clearTimeMarker()
        
    @pyqtSlot(int)
    def showSticksSlot(self,state):
        self.ui.skeletonPlot.showSticks = self.ui.showSticksCheckbox.isChecked()
        
    @pyqtSlot(int)
    def showTrajectoriesSlot(self,state):
        fig = self.ui.skeletonPlot
        fig.showTrajectory = self.ui.showTrajectoriesCheckbox.isChecked()
        #fig.lines = sum([fig.ax.plot([], [], [], '-', c=c) for c in fig.colors], [])
        self.ui.skeletonPlot.init(self.currTime)
        
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
        #self.setParent(mainWindow)
        
    def init(self, start=0):
        self.mainWindow.start = start
        self.mainWindow.ui.updateCurrTime(start)
        for line, pt in zip(self.lines, self.pts):
            # trajectory lines
            line.set_data([], [])
            line.set_3d_properties([])
            # points
            pt.set_data([], [])
            pt.set_3d_properties([])
        for stick_line in self.stick_lines:
            stick_line = self.ax.plot([], [], [], 'k-')[0]
        return self.lines + self.pts + self.stick_lines
    
    def animate(self, fileName):
        f= open(fileName, 'r')
        headers=f.readline().split()
        # A fix for a bug that misarranged the columns names in the file 
        headers = jointsMap.getFileHeader(headers)
        print headers
        self.hirarchy = jointsMap.getHirarchy(headers)
        joints = jointsMap.getJoints(headers)
        print joints
        jointsNum = len(joints)
        fileLength=0
        for line in f:
            fileLength+=1
        self.mainWindow.ui.slider.setRange(0, fileLength)
        self.mainWindow.ui.skeletonFileLength = fileLength
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
        a = np.linspace(0, 1, jointsNum)
        #self.colors = plt.cm.jet(a)
        from matplotlib.cm import _generate_cmap
        cm= _generate_cmap('Spectral', 256)
        self.colors = cm(a)
        self.colors[8] = [0, 0, 0, 1]
        #cm = matplotlib.colors.LinearSegmentedColormap('jet')
        
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
        #self.ax.view_init(30, 0)
        #self.ax.set_aspect('auto')
        def myAnimate(i):
            if self.mainWindow.pause or self.mainWindow.stop:
                self.draw()
                return self.lines + self.pts + self.stick_lines
            currTime = self.mainWindow.currTime+1
            self.mainWindow.ui.updateCurrTime(currTime)
            for line, pt, xi in zip(self.lines, self.pts, x_t):
                x, y, z = xi[self.mainWindow.start:currTime].T 
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
                else:    
                    for stick_line, (sp, ep) in zip(self.stick_lines, self.hirarchy):
                        stick_line._verts3d = x_t[[sp,ep], currTime, :].T.tolist()
            else:
                for stick_line in self.stick_lines:
                    stick_line._verts3d = [[],[],[]]
                    
            if self.rotate:
                self.ax.view_init(30, currTime)
            return self.lines + self.pts + self.stick_lines
        print self.mainWindow.playingSpeed
        return animation.FuncAnimation(
                    fig, myAnimate,init_func=self.init, interval=1000/self.mainWindow.playingSpeed, blit=True)

if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    mw = MainWindow()
    mw.show()
    sys.exit(app.exec_())
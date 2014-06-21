from PyQt4.QtGui import QCheckBox, QVBoxLayout, QPushButton, QLineEdit,\
     QWidget, QGridLayout, QFileDialog
from PyQt4.QtCore import QObject
import numpy as np
import utils.MovingAverage as ma
from matplotlib import pyplot as plt
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg \
                                                as FigureCanvas
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QTAgg \
                                                 as NavigationToolbar
import os
import importlib
                                                 
class AnalysisEditor(QWidget):
    def __init__(self, ui):
        QWidget.__init__(self)
        self.ui = ui
        self.chooseAnalysis = QPushButton()
        self.chooseAnalysis.setText("Choose Analysis")
        self.chooseAnalysis.setFixedWidth(100)
        self.lineEdit = QLineEdit()
        self.chooseAnalysis.clicked.connect(self.selectAnalysis)
        self.analysisFig = plt.figure()
        self.analysisFig.patch.set_facecolor('white')
        self.analysisFig.clf()
        self.analysisCanvas = FigureCanvas(self.analysisFig)
        self.toolbar = NavigationToolbar(self.analysisCanvas, self)
        self.analysisOperationsLayout = self.createOperationsLayout()     
        self.analysisAx = self.analysisFig.add_subplot(1,1,1)
        #self.gridLayout.addLayout(analysisOperationsLayout,1,7)
    
    def initCanvas(self):
        self.lineEdit.clear()
        self.analysisAx.cla()
        self.analysisAx = self.analysisFig.add_subplot(1,1,1)  
        self.analysisCanvas.draw()    
        
    def analysisOptionHandler(self):
        sender = self.sender()
        if sender.isChecked():
            vec = sender.getVec()
            sender.line = self.plotAnalysis(vec)
            #sender.line, = self.analysisAx.plot(sender.getVec())
        else:
            sender.line.remove()
        self.analysisCanvas.draw()
    
    def prepareCheckBox(self, getVec, label):
        operationCheck = QCheckBox()
        operationCheck.setText(label)
        operationCheck.setFixedWidth(100)
        operationCheck.getVec = getVec
        operationCheck.clicked.connect(self.analysisOptionHandler) 
        return operationCheck
    
    def Original(self):
        self.analysisVec = self.original.vec
        return self.analysisVec 
    
    def Derivative(self):
        self.analysisVec = np.diff(self.analysisVec)
        return self.analysisVec
    
    def LPF(self):
        self.analysisVec =  ma.movingAverage(self.analysisVec, 30, 1.1)
        return self.analysisVec
    
    def cluster(self):
        pass
    
    def createOperationsLayout(self):
        analysisOptionsLayout = QVBoxLayout()
        self.original = self.prepareCheckBox(self.Original, 'Original') 
        analysisOptionsLayout.addWidget(self.original)
        analysisOptionsLayout.addWidget(self.prepareCheckBox(self.LPF, 'LPF'))
        analysisOptionsLayout.addWidget(self.prepareCheckBox(self.Derivative, 'Derivative'))
        analysisOptionsLayout.addWidget(self.prepareCheckBox(self.cluster, 'cluster'))
        return analysisOptionsLayout
        
    def selectAnalysis(self):
        dlg = QFileDialog()
        dlg.setDirectory('Laban/analysis')
        analysisFile= unicode(dlg.getOpenFileName(filter='*.py'))
        self.lineEdit.setText(analysisFile)
        if not os.path.isfile(analysisFile):
            return
        rel = os.path.relpath(analysisFile).split('.')[-2]
        rel = rel.replace('\\','.')#[1:]
        analayzer = importlib.import_module(rel)
        self.analysisVec = analayzer.analyze(self.ui.selectedFile)
        self.original.line = self.plotAnalysis(self.analysisVec)
        self.original.vec = self.analysisVec
        self.original.setChecked(True)
    
    def plotAnalysis(self, vec):
        max_height = np.max(vec)
        min_height = np.min(vec)
        ax = self.analysisAx
        ax.set_ylim(min_height, max_height)
        line, = ax.plot(vec)
        self.analysisCanvas.draw()
        return line
    
    def clearTimeMarker(self):
        self.syncSkeletonWithAnalysis = False
        self.analysisTimeLine.remove()
        self.analysisCanvas.draw()

    def initTimeMarker(self):
        ax = self.analysisAx
        self.analysisBackground = self.analysisCanvas.copy_from_bbox(ax.bbox)
        vec = self.analysisVec
        max_height = np.max(vec)
        min_height = np.min(vec)
        y1 = [min_height, max_height]
        x1 = [0, 0]
        self.analysisTimeLine, = ax.plot(x1,y1,color='r',animated=True,label='timeMarker') 
        self.updateAnalysisTimeMarker()
        
    def updateAnalysisTimeMarker(self):
        self.analysisCanvas.restore_region(self.analysisBackground)
        currTime = self.ui.mainWindow.currTime
        x1 = [currTime,currTime]
        self.analysisTimeLine.set_xdata(x1)
        self.analysisAx.draw_artist(self.analysisTimeLine)
        self.analysisCanvas.blit(self.analysisAx.bbox)
        
    def prepareAnalysisEditorBeforeSync(self, handler):
        self.analysisCanvas.mpl_connect('button_press_event',handler)
        #self.analysisCanvas.draw()
        #self.updateAnalysisTimeMarker()
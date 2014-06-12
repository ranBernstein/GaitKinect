from PyQt4.QtGui import QLabel
from PyQt4.QtCore import pyqtSlot,SIGNAL,SLOT

class ClickableQLabel(QLabel):

    def __init(self, parent):
        QLabel.__init__(self, parent)

    def mouseReleaseEvent(self, ev):
        self.emit(SIGNAL('clicked()'))
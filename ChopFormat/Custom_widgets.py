from PyQt5 import QtCore, QtGui, QtWidgets

class PainterLabel(QtWidgets.QLabel):
    def __init__(self, brushsize):
        super().__init__()
        self.brushsize = brushsize
        self.x0 = 0
        self.y0 = 0
        self.x1 = 0
        self.y1 = 0
        self.flag = False
        self.upleftx, self.uplefty = 0, 0
    def mousePressEvent(self,event):
        self.flag = True
        self.x0 = event.x()
        self.y0 = event.y()


    def mouseReleaseEvent(self,event):
        self.flag = False

    def mouseMoveEvent(self,event):
        if self.flag:
            self.x1 = event.x()
            self.y1 = event.y()

            self.upleftx, self.uplefty = min(self.x0, self.x1), min(self.y0, self.y1)

            self.update()

    def paintEvent(self, event):
        super().paintEvent(event)
        rect = QtCore.QRect(self.upleftx, self.uplefty, abs(self.x1-self.x0), abs(self.y1-self.y0))
        painter = QtGui.QPainter(self)
        painter.setPen(QtGui.QPen(QtGui.QColor(255, 127, 25), self.brushsize, QtCore.Qt.DashLine))
        painter.drawRect(rect)

    def getRect(self):
        return self.upleftx, self.uplefty, abs(self.x1-self.x0), abs(self.y1-self.y0)
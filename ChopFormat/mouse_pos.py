import sys
# from PyQt5.QtWidgets import (QApplication, QLabel, QWidget)
from PySide2 import QtCore, QtWidgets, QtGui

class MouseTracker(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.setMouseTracking(True)

    def initUI(self):
        self.img = QtWidgets.QLabel(self)
        self.img.setPixmap(QtGui.QPixmap('C:/Users/Administrator/Desktop/0129/0818.png'))
        self.setGeometry(300, 300, 300, 200)
        self.setWindowTitle('Mouse Tracker')
        self.label = QtWidgets.QLabel(self)

        self.label.resize(200, 40)
        self.img.resize(400, 800)
        self.show()

    def mouseMoveEvent(self, event):
        self.label.setText('Mouse coords: ( %d : %d )' % (event.x(), event.y()))


if __name__ == '__main__':
    app = QtWidgets.QApplication()
    ex = MouseTracker()
    sys.exit(app.exec_())
import sys
# import PyQtUI4#调用ui模块
from PyQt5.QtWidgets import QApplication, QMainWindow
from Window_complete import CMWindow
from PyQt5 import QtCore, QtGui, QtWidgets

if __name__ == '__main__':
    app = QApplication(sys.argv)
    MainWindow = QMainWindow()
    ui = CMWindow(MainWindow)
    # print(ui)
    MainWindow.showMaximized()
    # print(MainWindow.size())
    # MainWindow.show()
    sys.exit(app.exec_())
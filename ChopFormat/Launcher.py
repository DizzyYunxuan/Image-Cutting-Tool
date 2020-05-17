import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from Window_complete import CMWindow

if __name__ == '__main__':
    app = QApplication(sys.argv)
    MainWindow = QMainWindow()
    ui = CMWindow(MainWindow)
    MainWindow.showMaximized()
    sys.exit(app.exec_())
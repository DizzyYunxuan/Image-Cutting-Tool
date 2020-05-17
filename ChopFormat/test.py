from PyQt5.QtWidgets import QApplication, QMainWindow
from uitest_review import Ui_MainWindow  # import the UI module

# set up a class for main window
class window(QMainWindow):
    def __init__(self, parent=None):
        super(window, self).__init__(parent)

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.Open.clicked.connect(self.openwindow)

    def openwindow(self):
        windownum = self.ui.windownum.value()
        print("open window num:", windownum)
        opennewwindow = newwindow(self)
        opennewwindow.show()

class newwindow(QMainWindow):
    def setupUi(self, MainWindow):
    MainWindow.setObjectName("MainWindow")

if __name__ == "__main__":
    app = QApplication([])
    gui = window()
    gui.show()
    app.exec_()
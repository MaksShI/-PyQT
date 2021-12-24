import sys
from PyQt5 import QtWidgets
import testingapp


class MyWindow(QtWidgets.QWidget):
    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)
        self.ui = testingapp.Ui_Form()
        self.ui.setupUi(self)
        self.ui.pushButton.clicked.connect(self.printString)
        self.ui.pushButton_2.clicked.connect(self.printString)
        self.ui.pushButton_3.clicked.connect(self.init_message)

    def printString(self):
        self.string = self.ui.textBrowser.text()
        print(self.string)

    def init_message(self):
        self.messages_init = self.ui.lineEdit.text()
        print(self.messages_init)


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = MyWindow()
    window.show()
    sys.exit(app.exec_())

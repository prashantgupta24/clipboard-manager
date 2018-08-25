import sys
from PyQt5.Qt import QApplication, QClipboard
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QPlainTextEdit
from PyQt5.QtCore import QSize

class Clippy(QWidget):
    def __init__(self):
        super().__init__()
        #self.setMinimumSize(QSize(440, 240))
        self.setWindowTitle("Clippy")

        b = QtWidgets.QPushButton('Push Me')
        b.height=60
        b.setToolTip('This is an example button')
        b.clicked.connect(lambda: self.onClick("hello"))

        h_box = QtWidgets.QHBoxLayout()
        h_box.addStretch()
        h_box.addWidget(b, 1)
        h_box.addStretch()

        v_box = QtWidgets.QVBoxLayout()
        v_box.addLayout(h_box)

        self.setLayout(v_box)


        # Add text field
        # self.b = QPlainTextEdit(self)
        # self.b.insertPlainText("Use your mouse to copy text to the clipboard.\nText can be copied from any application.\n")
        # self.b.move(10,10)
        # self.b.resize(400,200)
        #
        # QApplication.clipboard().dataChanged.connect(self.clipboardChanged)

    # Get the system clipboard contents

    def onClick(self, string):
        print(string)
    def clipboardChanged(self):
        text = QApplication.clipboard().text()
        print(text)
        self.b.insertPlainText(text + '\n')

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    root = Clippy()
    root.show()
    sys.exit(app.exec_())

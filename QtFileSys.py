import pyqtgraph as pg
from pyqtgraph.Qt import QtCore, QtGui, QtWidgets

class BrowserManager:
    def __init__(self, title: str, layout: QtWidgets.QVBoxLayout | QtWidgets.QHBoxLayout):

        self.title: str = title

        self.label = QtWidgets.QLabel("Save Path")

        self.textBox = QtWidgets.QLineEdit()

        self.browseButton = QtWidgets.QPushButton("Browse")

        self.browserManagerLayout = QtWidgets.QHBoxLayout()

        self.browserManagerLayout.addWidget(self.label)

        self.browserManagerLayout.addWidget(self.textBox)

        self.browserManagerLayout.addWidget(self.browseButton)

        layout.addLayout(self.browserManagerLayout)

        self.browseButton.clicked.connect(self.browseFile)

    def browseFile(self) -> str:
        fileName, _ = QtWidgets.QFileDialog.getOpenFileName(self.browseButton, self.title)
        if(fileName):
            self.textBox.setText(fileName)
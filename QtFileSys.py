import pyqtgraph as pg
from pyqtgraph.Qt import QtCore, QtGui, QtWidgets

#Instantiates a widget to either enter a filename, or browse for a file in the sysyem
class BrowserManager:
    def __init__(self, title: str, layout: QtWidgets.QBoxLayout):

        self.title: str = title

        #label
        self.label = QtWidgets.QLabel("Save Path")

        #enter filename here in gui
        self.textBox = QtWidgets.QLineEdit()

        #click this to open file manager
        self.browseButton = QtWidgets.QPushButton("Browse")

        self.browserManagerLayout = QtWidgets.QHBoxLayout()

        self.browserManagerLayout.addWidget(self.label)

        self.browserManagerLayout.addWidget(self.textBox)

        self.browserManagerLayout.addWidget(self.browseButton)

        layout.addLayout(self.browserManagerLayout)

        #calls the browseFile method whenever the browse button is pressed
        self.browseButton.clicked.connect(self.browseFile)

    #opens OS file manager and sets text box content to selected file
    def browseFile(self) -> str:
        fileName, _ = QtWidgets.QFileDialog.getOpenFileName(self.browseButton, self.title)
        if(fileName):
            self.textBox.setText(fileName)
import numpy
import pyqtgraph as pg
from pyqtgraph.Qt import QtCore, QtGui, QtWidgets

'''
Class to instantiate a slider to be inserted into a pyqtgraph window

low: int := min value of slider
high: int := max value of slider
'''

class Slider:
    def __init__(self, low: int, high: int, layout: QtWidgets.QVBoxLayout):
        self.low: int = low
        self.high: int = high
        self.val: int = self.low

        self.label = QtWidgets.QLabel('Trigger:\n' + str(self.val))
        layout.addWidget(self.label)

        self.slider = QtWidgets.QSlider(QtCore.Qt.Vertical)
        self.slider.setMinimum(self.low)
        self.slider.setMaximum(self.high)
        self.slider.setValue(self.val)
        

        self.slider.valueChanged.connect(self.setVal)

        layout.addWidget(self.slider)


    def setVal(self, val: int) -> None:
        self.label.setText('Trigger:\n' + str(val))
        self.val = val

    def getVal(self) -> int:
        return self.val


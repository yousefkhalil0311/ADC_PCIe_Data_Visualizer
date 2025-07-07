import numpy
import pyqtgraph as pg
from pyqtgraph.Qt import QtCore, QtGui, QtWidgets

'''
Class to instantiate a slider to be inserted into a pyqtgraph window

low: int := min value of slider
high: int := max value of slider
'''

class Slider:
    def __init__(self, title: str, unit: str, low: int, high: int, default: int, layout: QtWidgets.QVBoxLayout | QtWidgets.QHBoxLayout, orientation):
        self.low: int = low
        self.high: int = high
        self.val: int = default
        self.title: str = title
        self.unit: str = unit

        self.label = QtWidgets.QLabel("Uninitialized Label")
        self.setVal(self.val)

        layout.addWidget(self.label)

        self.slider = QtWidgets.QSlider(orientation)
        self.slider.setMinimum(self.low)
        self.slider.setMaximum(self.high)
        self.slider.setValue(self.val)
        

        self.slider.valueChanged.connect(self.setVal)

        layout.addWidget(self.slider)


    def setVal(self, val: int) -> None:
        self.val = val
        self.label.setText(f"{self.title}\n{str(self.val)} {self.unit}")

    def getVal(self) -> int:
        return self.val


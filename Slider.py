import numpy
import pyqtgraph as pg
from pyqtgraph.Qt import QtCore, QtGui, QtWidgets

'''
Class to instantiate a slider to be inserted into a pyqtgraph window

low: int := min value of slider
high: int := max value of slider
'''

class Slider:
    def __init__(self, title: str, unit: str, low: int, high: int, default: int, layout: QtWidgets.QBoxLayout, orientation):

        #set instance params
        self.low: int = low
        self.high: int = high
        self.val: int = default
        self.title: str = title
        self.unit: str = unit

        self.label = QtWidgets.QLabel("Uninitialized Label")
        self.setVal(self.val)

        #add label to layout
        layout.addWidget(self.label)

        #set slider params
        self.slider = QtWidgets.QSlider(orientation)
        self.slider.setMinimum(self.low)
        self.slider.setMaximum(self.high)
        self.slider.setValue(self.val)
        
        #attach setVal callback to react to slider changes
        self.slider.valueChanged.connect(self.setVal)

        #add slider to layout
        layout.addWidget(self.slider)


    #sets the value of the slider
    def setVal(self, val: int) -> None:
        self.val = val
        self.label.setText(f"{self.title}\n{str(self.val)} {self.unit}")

    #gets the value of the slider
    def getVal(self) -> int:
        return self.val


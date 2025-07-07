import numpy as np
import pyqtgraph as pg
from pyqtgraph.Qt import QtCore, QtGui, QtWidgets

class Plot:

    #each Plot will represent the data from one ADC channel on the connected hardware
    def __init__(self, title: str, unit: str, y_min: int, y_max: int, x_width : int, window : pg.GraphicsLayoutWidget):
        self.title : str = title
        self.SAMPLE_SIZE : int = x_width
        self.threshold: int = 0
        self.x : np.ndarray = np.arange(0, self.SAMPLE_SIZE, self.SAMPLE_SIZE / x_width)
        self.y : np.ndarray = np.zeros(x_width)
        self.plot = window.addPlot()
        self.plot.setTitle(title)
        self.plot.setLabel('bottom', 'Sample', units='')
        self.plot.setLabel('left', 'Amplitude', units=unit)
        self.plot.enableAutoRange(axis='y', enable=False)
        self.plot.setYRange(y_min, y_max)

        self.curve = self.plot.plot(self.x, self.y, pen='y')


    def update(self, newPlotData : np.ndarray) -> None :
        
        if newPlotData is None:
            return
        
        SAMPLE_SIZE : int = self.SAMPLE_SIZE

        thresholdIndex: int = 0

        for index, sampleVal in enumerate(newPlotData):
            if sampleVal == self.threshold:
                thresholdIndex = index
                break

        view: np.ndarray = newPlotData[thresholdIndex : len(newPlotData)]

        self.y = view.copy()

        if len(self.y) > SAMPLE_SIZE :
            self.y = self.y[0 : SAMPLE_SIZE]
        else:
            self.y = np.pad(self.y, (0, SAMPLE_SIZE - len(self.y)), constant_values=0)

        if(self.y.size % SAMPLE_SIZE == 0):
            self.curve.setData(self.x, self.y)
        

    def setThreshold(self, threshold: int) -> None:
        self.threshold = threshold
        

    def setRange(self, y_min: int, y_max: int) -> None:
        self.plot.setYRange(y_min, y_max)
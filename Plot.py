import numpy as np
import pyqtgraph as pg
from pyqtgraph.Qt import QtCore, QtGui, QtWidgets

class Plot:

    #each Plot will represent the data from one ADC channel on the connected hardware
    def __init__(self, ADCchannel : str, x_width : int, window : pg.GraphicsLayoutWidget):
        self.ADCchannel : str = ADCchannel
        self.SAMPLE_SIZE : int = x_width
        self.x : np.ndarray = np.arange(0, SAMPLE_SIZE, SAMPLE_SIZE / x_width)
        self.y : np.ndarray = np.zeros(x_width)
        self.plot = window.addPlot()
        self.plot.setTitle(ADCchannel)
        self.plot.setLabel('bottom', 'Sample', units='')
        self.plot.setLabel('left', 'Voltage', units='mV')
        self.plot.enableAutoRange(axis='y', enable=True)
        #self.plot.setYRange(0, 5000)

        self.curve = self.plot.plot(self.x, self.y, pen='y')

    def update(self, newPlotData : np.ndarray) -> None :
        
        if newPlotData is None:
            return
        
        SAMPLE_SIZE : int = self.SAMPLE_SIZE
        
        if len(newPlotData) != SAMPLE_SIZE:
            return 

        self.y = newPlotData.copy()

        
        if(self.y.size % SAMPLE_SIZE == 0):
            self.curve.setData(self.x, self.y)
        
#python includes
import numpy as np
import pyqtgraph as pg
from pyqtgraph.Qt import QtCore, QtGui, QtWidgets
import time
import struct

#project specific include
from Plot import Plot


#name of pcie device to connect to
defaultDevice = '/dev/xdma0_c2h_0'

#FFT size the Zynq FPGA
SAMPLE_SIZE = 128

#Function definitions begin

#gets data currently stored in RAM (circular buffer). Should start capturing data of size SAMPLE_SIZE once the voltage hits trigger threshold.
def getPCIeData(channel : str) -> np.ndarray | None: #return array of 32 bit words

    return None
    
app = pg.mkQApp("ADC_PCIe_Data_Visualizer")

#Function definitions end

#window is dynamically resizable. Start with small window size for compatibility 
win = pg.GraphicsLayoutWidget(show=True)
win.setWindowTitle("ADC Visualizer")
win.resize(640, 480)

#set antialiasing for better looking plots
pg.setConfigOptions(antialias=True)
pg.setConfigOptions(useOpenGL=True)


#initialize and draw all plots
plot1 = Plote('1', SAMPLE_SIZE, win)

#update all plots
def updateall():
    try:
        plot1.update(getPCIeData('1'))
    except Exception as e:

        #close window in case of failure
        win.close()
        print(f'Communication failure...{e}\n')


timer = QtCore.QTimer()
timer.timeout.connect(updateall)
timer.start(0)


#show window and execute plot updates
win.show()
pg.exec()

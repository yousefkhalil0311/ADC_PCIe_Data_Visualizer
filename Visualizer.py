#python includes
import os
import mmap
import numpy as np
import pyqtgraph as pg
from pyqtgraph.Qt import QtCore, QtGui, QtWidgets
import time
import struct

#project specific include
from Plot import Plot


#name of pcie device to connect to
PCIe_Device: str = '/dev/xdma0_c2h_0'
sharedmemFile: str = '/dev/shm/xdmaPythonStream'

#FFT size the Zynq FPGA
SAMPLE_SIZE: int = 512
BUFFER_SIZE: int = 1024 * SAMPLE_SIZE*4

with open(sharedmemFile, "wb") as f:
    f.truncate(BUFFER_SIZE)

with open(sharedmemFile, "r+b") as f:
    mm = mmap.mmap(f.fileno(), BUFFER_SIZE, access=mmap.ACCESS_READ)

#Function definitions begin

#gets data currently stored in RAM (circular buffer). Should start capturing data of size SAMPLE_SIZE once the voltage hits trigger threshold.
def getPCIeData(threshold: int, numValues: int) -> np.ndarray | None: #return array of 32 bit words

    try:
        mm.seek(0)
        threshold_index: int = 0

        while threshold_index < SAMPLE_SIZE:
            val : int = struct.unpack_from("<i", mm, threshold_index*4)[0]
            if(val >= threshold):
                break
            threshold_index += 1
        
        print(threshold_index)
        mm.seek(threshold_index * 4)

        data: bytes = mm.read(numValues * 4)
        return np.frombuffer(data, dtype=np.dtype('<i4'))
    
    except KeyboardInterrupt:
        print("Done.")
    finally:
        pass
        #mm.close()

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
plot1 = Plot('1', SAMPLE_SIZE, win)

#update all plots
def updateall():
    try:
        a: np.ndarray = getPCIeData(np.random.randint(1, 200), plot1.SAMPLE_SIZE)
        print("Received: ", a)
        plot1.update(a)
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

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
from Slider import Slider


#name of pcie device to connect to
PCIe_Device: str = '/dev/xdma0_c2h_0'
sharedmemFile: str = '/dev/shm/xdmaPythonStream'

#FFT size the Zynq FPGA
SAMPLE_SIZE: int = 64
BUFFER_SIZE: int = 1024 * SAMPLE_SIZE*4

'''
with open(sharedmemFile, "wb") as f:
    f.truncate(BUFFER_SIZE)

with open(sharedmemFile, "r+b") as f:
    mm = mmap.mmap(f.fileno(), BUFFER_SIZE, access=mmap.ACCESS_READ)
'''

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

window = QtWidgets.QWidget()

main_layout = QtWidgets.QVBoxLayout()

window.setLayout(main_layout)

layout = QtWidgets.QHBoxLayout()

main_layout.addLayout(layout)

#initialize and draw all sliders
slider1 = Slider(0, 200, layout)


#window is dynamically resizable. Start with small window size for compatibility 
graph = pg.GraphicsLayoutWidget(show=True)
graph.setWindowTitle("ADC Visualizer")
#graph.resize(640, 480)

layout.addWidget(graph)

#set antialiasing for better looking plots
pg.setConfigOptions(antialias=True)
pg.setConfigOptions(useOpenGL=True)

#initialize and draw all plots
plot1 = Plot('ADC Channel 1 Data', SAMPLE_SIZE, graph)


#update all plots
def updateall():
    try:
        a: np.ndarray = np.random.randint(low=0, high=200, size=plot1.SAMPLE_SIZE * 20)#getPCIeData(np.random.randint(1, 200), plot1.SAMPLE_SIZE)
        #print("Received: ", a)
        plot1.setThreshold(slider1.getVal())
        plot1.update(a)
    except Exception as e:

        #close window in case of failure
        graph.close()
        print(f'Communication failure...{e}\n')


timer = QtCore.QTimer()
timer.timeout.connect(updateall)
timer.start(100)


#show window and execute plot updates
window.show()
pg.exec()

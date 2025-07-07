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
from QtButtons import RadioButton
from QtButtons import CheckBox
from QtButtons import PushButton
from QtFileSys import BrowserManager
from ParamTable import ParamTable
from ParamTable import ParamRow



#name of pcie device to connect to
PCIe_Device: str = '/dev/xdma0_c2h_0'
sharedmemFile: str = '/dev/shm/xdmaPythonStream'

#Sample Depth
SAMPLE_SIZE: int = 512
BUFFER_SIZE: int = 20 * SAMPLE_SIZE * 4

#Graph Parameters
PLOT_UNITS: str = 'mV'
MIN_PLOT_VALUE: int = 0
MAX_PLOT_VALUE: int = 200

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

plotLayout = QtWidgets.QHBoxLayout()

DDCTable: ParamTable = ParamTable('CH', 'Enable', 'Param', 'DDC1', 'DDC2', 'DDC3')

channel0Row: ParamRow = ParamRow(DDCTable.VerticalLayout, QtWidgets.QLabel('0'), QtWidgets.QCheckBox(), QtWidgets.QLabel('0'), QtWidgets.QLineEdit(), QtWidgets.QLineEdit(), QtWidgets.QLineEdit())

triggerLayout = QtWidgets.QVBoxLayout()

pathOptions: RadioButton = RadioButton('System Capture', triggerLayout, 'Active', 'Disabled', default='Active')

#initialize and draw all sliders
triggerSlider: Slider = Slider('Trigger', PLOT_UNITS, MIN_PLOT_VALUE, MAX_PLOT_VALUE, MIN_PLOT_VALUE, triggerLayout, QtCore.Qt.Vertical)

pathOptions: RadioButton = RadioButton('Edge', triggerLayout, 'Rising', 'Falling', 'Any', default='Rising')

plotLayout.addLayout(triggerLayout)

#window is dynamically resizable. Start with small window size for compatibility 
graph = pg.GraphicsLayoutWidget(show=True)
graph.setWindowTitle("ADC Visualizer")

#initialize and draw all plots
plot1: Plot = Plot('ADC Sample Data', PLOT_UNITS, MIN_PLOT_VALUE, MAX_PLOT_VALUE, SAMPLE_SIZE, graph)

plotLayout.addWidget(graph)

main_layout.addLayout(plotLayout)

attSliderLayout = QtWidgets.QHBoxLayout()

pathOptions: RadioButton = RadioButton('Select Path', attSliderLayout, '500MHz LP', '1GHz LP', '2GHz LP', 'Bypass', default='500MHz LP')

attenuationSlider: Slider = Slider('Attenuation', 'dB', 0, 32, 32, attSliderLayout, QtCore.Qt.Horizontal)

calEnable: CheckBox = CheckBox('Calibration Mode', attSliderLayout)

main_layout.addLayout(attSliderLayout)

row3Layout = QtWidgets.QHBoxLayout()

fileBrowser: BrowserManager = BrowserManager('Select File for Capture', row3Layout)

numSamplesOrTime: RadioButton = RadioButton('Aquire by', row3Layout, '# of Samples', 'time(us)', default='# of Samples')

textBox: QtWidgets.QLineEdit = QtWidgets.QLineEdit()

textBox.setMaxLength(12)
textBox.setFixedWidth(8 * 12)

row3Layout.addWidget(textBox)

captureButton: PushButton = PushButton('Capture', row3Layout, lambda: print('Capturing!!!!'))

main_layout.addLayout(row3Layout)



#set antialiasing for better looking plots
pg.setConfigOptions(antialias=True)
pg.setConfigOptions(useOpenGL=True)



#update all plots
def updateall():
    try:
        a: np.ndarray = np.random.randint(low=0, high=200, size=plot1.SAMPLE_SIZE * 20)#getPCIeData(np.random.randint(1, 200), plot1.SAMPLE_SIZE)
        
        plot1.setThreshold(triggerSlider.getVal())

        plot1.update(a)
    except Exception as e:

        #close window in case of failure
        graph.close()
        print(f'Communication failure...{e}\n')


timer = QtCore.QTimer()
timer.timeout.connect(updateall)
timer.start(0)


#show window and execute plot updates
window.show()
pg.exec()

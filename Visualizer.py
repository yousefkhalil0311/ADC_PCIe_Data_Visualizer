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
from ParamTools import ChannelControlWidget
from ParamTools import LabelColumn
from ParamTools import CheckBoxColumn
from ParamTools import LineEditColumn

#global parameter store & hardware controller
from QC_Controller import QueensCanyon



#name of pcie device to connect to
PCIe_Device: str = '/dev/xdma0_c2h_0'
sharedmemFile: str = '/dev/shm/xdmaPythonStream'

#Sample Depth
SAMPLE_SIZE: int = 512
BUFFER_SIZE: int = 100 * SAMPLE_SIZE * 4

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

leftPanel = QtWidgets.QVBoxLayout()

plotLayout.addLayout(leftPanel)

Ch0Widget: ChannelControlWidget = ChannelControlWidget(0, leftPanel)
Ch1Widget: ChannelControlWidget = ChannelControlWidget(1, leftPanel)
Ch2Widget: ChannelControlWidget = ChannelControlWidget(2, leftPanel)
Ch3Widget: ChannelControlWidget = ChannelControlWidget(3, leftPanel)
Ch4Widget: ChannelControlWidget = ChannelControlWidget(4, leftPanel)
Ch5Widget: ChannelControlWidget = ChannelControlWidget(5, leftPanel)
Ch6Widget: ChannelControlWidget = ChannelControlWidget(6, leftPanel)
Ch7Widget: ChannelControlWidget = ChannelControlWidget(7, leftPanel)


triggerLayout = QtWidgets.QVBoxLayout()

activateSetting: RadioButton = RadioButton('System', triggerLayout, 'Active', 'Disabled', default='Active')

#initialize and draw all sliders
triggerSlider: Slider = Slider('Trigger', PLOT_UNITS, MIN_PLOT_VALUE, MAX_PLOT_VALUE, 100, triggerLayout, QtCore.Qt.Vertical)

edgeSetting: RadioButton = RadioButton('Edge', triggerLayout, 'Rising', 'Falling', 'Any', default='Rising')

plotLayout.addLayout(triggerLayout)

#window is dynamically resizable. Start with small window size for compatibility 
graph = pg.GraphicsLayoutWidget(show=True)
graph.setWindowTitle("ADC Visualizer")

#initialize and draw all plots
plot1: Plot = Plot('ADC Sample Data', PLOT_UNITS, MIN_PLOT_VALUE, MAX_PLOT_VALUE, SAMPLE_SIZE, graph)

plotLayout.addWidget(graph)

graph.nextRow()

#initialize and draw all plots
plot2: Plot = Plot('ADC Sample Data', PLOT_UNITS, MIN_PLOT_VALUE, MAX_PLOT_VALUE, SAMPLE_SIZE, graph, True)

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

def callback():
    QueensCanyon.setParam("aquisitionTime(ms)", textBox.text())

textBox.editingFinished.connect(callback)

row3Layout.addWidget(textBox)

captureButton: PushButton = PushButton('Capture', row3Layout, lambda: print('Capturing!!!!'))

main_layout.addLayout(row3Layout)

QueensCanyon.saveParamsToJson()

#set antialiasing for better looking plots
pg.setConfigOptions(antialias=True)
pg.setConfigOptions(useOpenGL=True)

freq = 0

#update all plots
def updateall():

    global freq

    try:
        a: np.ndarray = (100 + (100 * np.sin(np.linspace(0, 2*np.pi * freq, SAMPLE_SIZE*20))).astype(int))[np.random.randint(0, 500):]
        
        freq = freq%100000 + 1

        plot1.setThreshold(triggerSlider.getVal())
        plot1.setTriggerEdge(edgeSetting.getSelectedRadioButton())

        plot1.update(a)
        plot2.update(a)


        QueensCanyon.saveParamsToJson()
        
    except Exception as e:

        #close window in case of failure
        graph.close()
        print(f'Communication failure...{e}\n')


timer = QtCore.QTimer()
timer.timeout.connect(updateall)
timer.start(10)


#show window and execute plot updates
window.show()
pg.exec()

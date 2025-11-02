#python includes
import os
import mmap
import numpy as np
import pyqtgraph as pg
from pyqtgraph.Qt import QtCore, QtGui, QtWidgets

#project specific include
from Plot import Plot
from Slider import Slider
from QtButtons import RadioButton
from QtButtons import CheckBox
from QtButtons import PushButton
from QtFileSys import BrowserManager
from ParamTools import ChannelControlWidget

#global parameter store & hardware controller
from QC_Controller import QueensCanyon

#database interface class
from paramWriter import databaseHandler
from paramWriter import paramWriter

#params needed to connect to database
path_to_serviceAccountKey: str = "secrets/db_accountkey.json"
databaseURL: str = "https://yksdb001-default-rtdb.firebaseio.com"
databaseReference: str = "QC_paramStore"

#name of pcie device to connect to
PCIe_Device: str = '/dev/xdma0_c2h_0'

#name of pcie device to connect to
PCIe_Device_command_stream: str = '/dev/xdma0_user'

sharedmemFile: str = '/dev/shm/xdmaPythonStream'

#Sample Depth
SAMPLE_SIZE: int = 32
BUFFER_SIZE: int = SAMPLE_SIZE*16

#Graph Parameters
PLOT_UNITS: str = 'mV'
MIN_PLOT_VALUE: int = -2000
MAX_PLOT_VALUE: int = 2000


paramDatabase: databaseHandler = databaseHandler(path_to_serviceAccountKey, databaseURL, databaseReference)

def onChange(event, data):

    if isinstance(data, dict):
        if data['data'] and isinstance(data['data'], dict):
            for key, value in data['data'].items():
                QueensCanyon.setParam(key, value)
            
            paramDatabase.databaseUpdatedFlag = True


paramDatabase.listen(onChange)


#initialize object to handle writing params to hardware BRAM
bramProgrammer: paramWriter = paramWriter(PCIe_Device_command_stream, 'config.json')

#keep a reference of all widget instances
widgetInstances: list = []

#with open(sharedmemFile, "wb") as f:
    #f.truncate(BUFFER_SIZE)

#with open(sharedmemFile, "r+b") as f:
    #mm = mmap.mmap(f.fileno(), BUFFER_SIZE, access=mmap.ACCESS_READ)


#Function definitions begin

#gets data currently stored in RAM (circular buffer). Should start capturing data of size SAMPLE_SIZE once the voltage hits trigger threshold.
def getPCIeData(numValues: int, offset: int) -> np.ndarray | None: #return array of 32 bit words

    try:
        mm.seek(0)

        #data stored as 16 bit values (I0, Q0, I1, Q1, I2, Q2, I3, Q3, 0, 0, 0, 0, 0, 0, 0, 0)
        data: bytes = mm.read(numValues * 2 * 16) #2 bytes per value, extract every 16th value
        return np.frombuffer(data, dtype=np.dtype('<i2'))[offset::16]
    
    except KeyboardInterrupt:
        print("Done.")
    finally:
        pass
        #mm.close()

    return None

#opens card to host interface
def openPCIeStream(stream: str) -> int:
    try:

        fd: int = os.open(stream, os.O_RDONLY)

        return fd
    
    except KeyboardInterrupt:
        print('Done. ')
    finally:
        pass

#closes card to host interface
def closePCIeStream(fd: int) -> int:
    try:

        os.close(fd)
    
    except KeyboardInterrupt:
        print('Done. ')
    finally:
        pass


def getPCIeChannelData(fd: int, numValues: int, channel: int, component: str) -> np.ndarray:
    
    componentMap: dict[str, int] = {
        'I': 0,
        'Q': 1
    }

    try:

        offset: int = channel * 2 + componentMap[component]

        data: bytes = os.read(fd, numValues * 2 * 16)

        returnBuffer: np.ndarray = np.frombuffer(data, dtype=np.dtype('<i2'))[offset:-1:16]

        return returnBuffer
    
    except KeyboardInterrupt:
        print('Done. ')
    finally:
        pass

#gets sample data over pcie and organizes into dictionary for each channel
def getPCIeStreamData(fd: int, numValues: int) -> dict[str, np.ndarray]:

    try:

        os.lseek(fd, 0, os.SEEK_SET)

        data: bytes = os.read(fd, numValues * 2 * 16)

        returnDict: dict[str, np.ndarray] = {
            'I0': np.frombuffer(data, dtype=np.dtype('<i2'))[0:-1:16],
            'Q0': np.frombuffer(data, dtype=np.dtype('<i2'))[1:-1:16],
            'I1': np.frombuffer(data, dtype=np.dtype('<i2'))[2:-1:16],
            'Q1': np.frombuffer(data, dtype=np.dtype('<i2'))[3:-1:16],
            'I2': np.frombuffer(data, dtype=np.dtype('<i2'))[4:-1:16],
            'Q2': np.frombuffer(data, dtype=np.dtype('<i2'))[5:-1:16],
            'I3': np.frombuffer(data, dtype=np.dtype('<i2'))[6:-1:16],
            'Q3': np.frombuffer(data, dtype=np.dtype('<i2'))[7:-1:16],
            'I4': np.frombuffer(data, dtype=np.dtype('<i2'))[8:-1:16],
            'Q4': np.frombuffer(data, dtype=np.dtype('<i2'))[9:-1:16],
            'I5': np.frombuffer(data, dtype=np.dtype('<i2'))[10:-1:16],
            'Q5': np.frombuffer(data, dtype=np.dtype('<i2'))[11:-1:16],
            'I6': np.frombuffer(data, dtype=np.dtype('<i2'))[12:-1:16],
            'Q6': np.frombuffer(data, dtype=np.dtype('<i2'))[13:-1:16],
            'I7': np.frombuffer(data, dtype=np.dtype('<i2'))[14:-1:16],
            'Q7': np.frombuffer(data, dtype=np.dtype('<i2'))[15:-1:16],
        }

        return returnDict

    except KeyboardInterrupt:
        print('Done.')
    
    finally:
        pass
    
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

#add widgets to list
widgetInstances += [Ch0Widget, Ch1Widget, Ch2Widget, Ch3Widget, Ch4Widget, Ch5Widget, Ch6Widget, Ch7Widget]

triggerLayout = QtWidgets.QVBoxLayout()

activateSetting: RadioButton = RadioButton('System', triggerLayout, 'Active', 'Disabled', default='Active')

#initialize and draw all sliders
triggerSlider: Slider = Slider('Trigger', PLOT_UNITS, MIN_PLOT_VALUE, MAX_PLOT_VALUE, 100, triggerLayout, QtCore.Qt.Vertical)

edgeSetting: RadioButton = RadioButton('Edge', triggerLayout, 'Rising', 'Falling', 'Any', default='Rising')

#add widgets to list
widgetInstances += [activateSetting, edgeSetting]

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

attenuationSlider: Slider = Slider('Attenuation', 'dB', 0, 31, 31, attSliderLayout, QtCore.Qt.Horizontal)

calEnable: CheckBox = CheckBox('Calibration Mode', attSliderLayout)

#add widgets to list
widgetInstances += [pathOptions, calEnable]

main_layout.addLayout(attSliderLayout)

row3Layout = QtWidgets.QHBoxLayout()

fileBrowser: BrowserManager = BrowserManager('Save File', row3Layout)

numSamplesOrTime: RadioButton = RadioButton('Aquire by', row3Layout, 'num of Samples', 'time(ms)', default='num of Samples')

textBox: QtWidgets.QLineEdit = QtWidgets.QLineEdit()

textBox.setMaxLength(12)
textBox.setFixedWidth(8 * 12)

def callback():
    QueensCanyon.setParam("aquisitionTime(ms)", int(textBox.text()))

textBox.editingFinished.connect(callback)

#add widgets to list
widgetInstances += [numSamplesOrTime]

row3Layout.addWidget(textBox)

captureButton: PushButton = PushButton('Capture', row3Layout, lambda: print('Capturing!!!!'))

main_layout.addLayout(row3Layout)

row4Layout = QtWidgets.QHBoxLayout()

stdinBrowser: BrowserManager = BrowserManager('Data Stream', row4Layout)

stdoutBrowser: BrowserManager = BrowserManager('Command Stream', row4Layout)

configBrowser: BrowserManager = BrowserManager('Config File', row4Layout)

main_layout.addLayout(row4Layout)

QueensCanyon.saveParamsToJson()

#set antialiasing for better looking plots (may reduce performance)
pg.setConfigOptions(antialias=False)
pg.setConfigOptions(useOpenGL=True)

freq = 0


#if instance connected to hardware, program hardware:
if os.path.exists(PCIe_Device_command_stream):
    bramProgrammer.setParamsTable()
    print(bramProgrammer.setupBRAM())

#if instance connected to hardware, open data stream:
if os.path.exists(PCIe_Device):
    fd: int = openPCIeStream(PCIe_Device)

paramChanged: bool = False

#update all plots
def updateall():

    global freq

    try:

        plot1.setThreshold(triggerSlider.getVal())
        plot1.setTriggerEdge(edgeSetting.getSelectedRadioButton())

        if os.path.exists(PCIe_Device):
            data: dict[str, np.ndarray] = getPCIeStreamData(fd, SAMPLE_SIZE)

        #display curves based on user selection
        if QueensCanyon.getParam("Channel 0-Enable") != 0:
            plot1.update(data['I0'], plot1.curve0)
            plot2.update(data['I0'], plot2.curve0)
        if QueensCanyon.getParam("Channel 1-Enable") != 0:
            plot1.update(data['I1'], plot1.curve1)
            plot2.update(data['I1'], plot2.curve1)
        if QueensCanyon.getParam("Channel 2-Enable") != 0:
            plot1.update(data['I2'], plot1.curve2)
            plot2.update(data['I2'], plot2.curve2)
        if QueensCanyon.getParam("Channel 3-Enable") != 0:
            plot1.update(data['I3'], plot1.curve3)
            plot2.update(data['I3'], plot2.curve3)
        if QueensCanyon.getParam("Channel 4-Enable") != 0:
            plot1.update(data['I4'], plot1.curve4)
            plot2.update(data['I4'], plot2.curve4)
        if QueensCanyon.getParam("Channel 5-Enable") != 0:
            plot1.update(data['I5'], plot1.curve5)
            plot2.update(data['I5'], plot2.curve5)
        if QueensCanyon.getParam("Channel 6-Enable") != 0:
            plot1.update(data['I6'], plot1.curve6)
            plot2.update(data['I6'], plot2.curve6)
        if QueensCanyon.getParam("Channel 7-Enable") != 0:
            plot1.update(data['I7'], plot1.curve7)
            plot2.update(data['I7'], plot2.curve7)

        #if parameters were updated, update the database
        if QueensCanyon.saveParamsToJson() == True:
            paramDatabase.setData(QueensCanyon.getParams())
            paramChanged = True
        
        #update app parameters if changes in database detected
        if paramDatabase.databaseUpdatedFlag == True:

            #reset databaseUpdatedFlag
            paramDatabase.databaseUpdatedFlag = False

            #update JSON with latest params
            QueensCanyon.saveParamsToJson()

            #update gui from paramStore
            for widget in widgetInstances:
                widget.update()

            paramChanged = True

        #if instance connected to hardware & paramChanged is True, program hardware:
        if os.path.exists(PCIe_Device_command_stream) and paramChanged:

            #program QC hardware
            changedIndex: int = bramProgrammer.getChangedParamIndex()
            bramProgrammer.setParamsTable()
            print(bramProgrammer.updateBRAM(changedIndex))

            #reset paramChanged flag
            paramChanged = False
            
        
    except Exception as e:

        #close stream and window in case of failure
        closePCIeStream(fd)
        graph.close()
        print(f'Communication failure...{e}\n')


timer = QtCore.QTimer()
timer.timeout.connect(updateall)
timer.start(100)


#show window and execute plot updates
window.show()
pg.exec()

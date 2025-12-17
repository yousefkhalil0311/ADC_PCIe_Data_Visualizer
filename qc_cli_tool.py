#python includes
import os
import mmap
import numpy as np
from pathlib import Path
from datetime import datetime
from QtFileSys import BrowserManager

#global parameter store & hardware controller
from QC_Controller import QueensCanyon

#bram parameter interface class
from paramWriter import paramWriter

#name of pcie device to connect to
PCIe_Device: str = '/dev/xdma0_c2h_0'

#command stream for PCIe device
PCIe_Device_command_stream: str = '/dev/xdma0_user'

#config file
configFileName: str = 'config.json'

#memory file to store data capture to
sharedmemFile: str = '/dev/shm/xdmaPythonStream'

#global file descriptor for data stream. Use for async captures
fd: int = -1

#config file path
configFilePath: str = f'{Path.cwd()}/{configFileName}'

#Load parameters from json config file to the QueensCanyon object
QueensCanyon.setConfigFile(configFileName)
QueensCanyon.getParamsFromJson()

SAMPLE_SIZE: int = QueensCanyon.getParam('num of Samples to get')
BUFFER_SIZE: int = SAMPLE_SIZE*16

#initialize object to handle writing params to hardware BRAM
bramProgrammer: paramWriter = paramWriter(PCIe_Device_command_stream, configFileName)

with open(sharedmemFile, "wb") as f:
    f.truncate(BUFFER_SIZE)

with open(sharedmemFile, "r+b") as f:
    mm = mmap.mmap(f.fileno(), BUFFER_SIZE, access=mmap.ACCESS_READ)

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

#get current time for file name
currentTimeStr: str = datetime.now().strftime("%Y-%m-%d_%H-%M-%S-%f")

#format save file for cwd/Captures/Capture_CurrentTime
saveFilePath: str = f'{Path.cwd()}/Captures/Capture_{currentTimeStr}.bin'

#if instance connected to hardware, program hardware:
if os.path.exists(PCIe_Device_command_stream):

    bramProgrammer.setParamsTable()
    print(bramProgrammer.setupBRAM())

else:

    print("Error: PCIe Device not detected")

#if instance connected to hardware, open data stream and capture data:
if os.path.exists(PCIe_Device):
    try:
        
        fd = openPCIeStream(PCIe_Device)
        #TODO Get data and store to file
        
    except Exception as e:

        #close stream and window in case of failure
        if fd > -1:
            closePCIeStream(fd)
            
        print(f'Communication failure...{e}\n')

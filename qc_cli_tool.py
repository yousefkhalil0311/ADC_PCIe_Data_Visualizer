#python includes
import os
import argparse
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
configFile: str = 'config.json'

#memory file to store data capture to
sharedmemFile: str = '/dev/shm/xdmaPythonStream'
sharedmemFilePath: str = Path(sharedmemFile)

#config file path
configFilePath: str = f'{Path.cwd()}/{configFile}'

#sample rate of the ADC system
SAMPLE_RATE: int = 250_000_000 #250MSps

#number of samples to take
SAMPLE_SIZE: int

#parse command line args
parser = argparse.ArgumentParser(description="ADC_PCIe_Data_Visualizer")

#config file argument
parser.add_argument("-c", "--configFile", help="JSON config file path/name.", default=configFilePath)

#parse args
args = parser.parse_args()


#update variables
configFile = args.configFile


#global file descriptor for data stream. Use for async captures
fd: int = -1

#Load parameters from json config file to the QueensCanyon object
QueensCanyon.setConfigFile(configFile)
QueensCanyon.getParamsFromJson()

#initialize object to handle writing params to hardware BRAM
bramProgrammer: paramWriter = paramWriter(PCIe_Device_command_stream, configFile)

#get current time for file name
currentTimeStr: str = datetime.now().strftime("%Y-%m-%d_%H-%M-%S-%f")

#format save file for cwd/Captures/Capture_CurrentTime
saveFilePath: str = f'{Path.cwd()}/Captures/Capture_{currentTimeStr}.bin'

#if instance connected to hardware, program hardware:
if os.path.exists(PCIe_Device_command_stream):

    print('validating params config file')
    bramProgrammer.setParamsTable()

    print('Programming Hardware')
    result: bool = bramProgrammer.setupBRAM()

    if result:
        print('Successfully programmed hardware')
    else:
        print('failed to program hardware')

else:

    print("Error: PCIe Device not detected")

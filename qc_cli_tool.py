#python includes
import os
import argparse
from pathlib import Path

#global parameter store & hardware controller
from QC_Controller import QueensCanyon

#bram parameter interface class
from paramWriter import paramWriter

#command stream for PCIe device
PCIe_Device_command_stream: str = '/dev/xdma0_user'

#config file
configFile: str = 'config.json'

#config file path
configFilePath: str = f'{Path.cwd()}/{configFile}'

#parse command line args
parser = argparse.ArgumentParser(description="ADC_PCIe_Data_Visualizer")

#config file argument
parser.add_argument("-c", "--configFile", help="JSON config file path/name.", default=configFilePath)

#parse args
args = parser.parse_args()


#update variables
configFile = args.configFile

#Load parameters from json config file to the QueensCanyon object
QueensCanyon.setConfigFile(configFile)
QueensCanyon.getParamsFromJson()

#initialize object to handle writing params to hardware BRAM
bramProgrammer: paramWriter = paramWriter(PCIe_Device_command_stream, configFile)

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

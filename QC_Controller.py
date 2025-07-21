
import json
import os
import struct

class QC_Controller:
    def __init__(self, h2cStream: str, c2hStream: str):
        self.h2c_path: str = h2cStream
        self.c2h_path: str = c2hStream
        self.paramStore: dict = {} 
        '''{
            'Channels': {
                'CH0_ENABLE': False,
                'CH1_ENABLE': False,
                'CH2_ENABLE': False,
                'CH3_ENABLE': False,
                'CH4_ENABLE': False,
                'CH5_ENABLE': False,
                'CH6_ENABLE': False,
                'CH7_ENABLE': False,
            },
            'DDC Blocks': {
                'Global Settings': {
                    'CH1': {
                        'Center Frequency (MHz)': 0,
                        'Output Sample Rate (Msps)': 1,
                    },
                    'CH2': {
                        'Center Frequency (MHz)': 0,
                        'Output Sample Rate (Msps)': 1,
                    },
                    'CH3': {
                        'Center Frequency (MHz)': 0,
                        'Output Sample Rate (Msps)': 1,
                    },
                },
                'DDC0': {
                    'CH1_ENABLE': False,
                    'CH2_ENABLE': False,
                    'CH3_ENABLE': False,
                },
                'DDC1': {
                    'CH1_ENABLE': False,
                    'CH2_ENABLE': False,
                    'CH3_ENABLE': False,
                },
                'DDC2': {
                    'CH1_ENABLE': False,
                    'CH2_ENABLE': False,
                    'CH3_ENABLE': False,
                },
                'DDC3': {
                    'CH1_ENABLE': False,
                    'CH2_ENABLE': False,
                    'CH3_ENABLE': False,
                },
                'DDC4': {
                    'CH1_ENABLE': False,
                    'CH2_ENABLE': False,
                    'CH3_ENABLE': False,
                },
                'DDC5': {
                    'CH1_ENABLE': False,
                    'CH2_ENABLE': False,
                    'CH3_ENABLE': False,
                },
                'DDC6': {
                    'CH1_ENABLE': False,
                    'CH2_ENABLE': False,
                    'CH3_ENABLE': False,
                },
                'DDC7': {
                    'CH1_ENABLE': False,
                    'CH2_ENABLE': False,
                    'CH3_ENABLE': False,
                },
            },
            'System': {
                'CAL EN': False,
                'System Active': True,
                'Filter Bank': '500MHz LP',
                'Aquire By numSamples': False,
                'Aquire By time(ms)': True,
                'Calibration length(ms)': 5,
                'AquisitionTime(ms)': 5
            }
        }'''

        self.paramToAddressMapping = [
            ("Channel 0-Enable", 0x00),
            ("Channel 1-Enable", 0x00),
            ("Channel 2-Enable", 0x00),
            ("Channel 3-Enable", 0x00),
            ("Channel 4-Enable", 0x00),
            ("Channel 5-Enable", 0x00),
            ("Channel 6-Enable", 0x00),
            ("Channel 7-Enable", 0x00),
            ("DDC 0-1", 0x00),
            ("SFout (Msps)-0", 0x00),
            ("SFout (Msps)-2", 0x00),
            ("SFout (Msps)-1", 0x00)
        ]
        self.configFile = 'config.json'

        if os.path.exists(self.configFile):
            with open(self.configFile, 'r') as configFile:
                self.paramStore = json.load(configFile)
        else:
            with open(self.configFile, 'w') as configFile:
                json.dump(self.paramStore, configFile, indent=4)

    def setConfigFile(self, fileName: str) -> None:
        self.configFile = fileName
        
    def setParam(self, key: str, value: any) -> None:
        self.paramStore[key] = value

    def getParam(self, key: str) -> any:
        return self.paramStore[key]

    def getParamsFromJson(self) -> dict:
        with open(self.configFile, 'r') as configFile:
            return json.load(configFile)
    
    def saveParamsToJson(self) -> None:

        if self.paramStore == self.getParamsFromJson():
            return
        
        with open(self.configFile, 'w') as configFile:
            json.dump(self.paramStore, configFile, indent=4)

    def loadParamsFromJson(self) -> None:
        with open(self.configFile, 'r') as configFile:
            self.paramStore = json.load(configFile)

    def programParam(self, key: str) -> None:
        pass

    def programAllParams(self) -> None:
        pass
    
QueensCanyon: QC_Controller = QC_Controller('', '')
import json
import os
import struct
from typing import Any

class QC_Controller:
    def __init__(self, h2cStream: str, c2hStream: str):
        self.h2c_path: str = h2cStream
        self.c2h_path: str = c2hStream

        self.paramStore: dict = {
            "Channel 0-Enable": 0,
            "Channel 1-Enable": 0,
            "Channel 2-Enable": 0,
            "Channel 3-Enable": 0,
            "Channel 4-Enable": 0,
            "Channel 5-Enable": 0,
            "Channel 6-Enable": 0,
            "Channel 7-Enable": 0,
            "DDC 0-1": 0,
            "DDC 0-2": 0,
            "DDC 0-3": 0,
            "Fmix (MHz)-0": 1,
            "Fmix (MHz)-1": 1,
            "Fmix (MHz)-2": 1,
            "SFout (Msps)-0": 1,
            "SFout (Msps)-1": 1,
            "SFout (Msps)-2": 1,
            "System-Active": 0,
            "System-Disabled": 0,
            "Select Path-500MHz LP": 1,
            "Select Path-Bypass": 0,
            "Select Path-2GHz LP": 0,
            "Select Path-1GHz LP": 0,
            "Aquire by-num of Samples": 0,
            "attenuation_binVal": 63,
            "Aquire by-time(us)": 1,
            "aquisitionTime(ms)": 10,
            "Calibration Mode": 0,
            "Edge-Rising": 1,
            "Edge-Falling": 0,
            "Edge-Any": 0,
            "num of Samples to get": 0
        } 

        self.configFile = 'config.json'

        if os.path.exists(self.configFile):
            with open(self.configFile, 'r') as configFile:
                self.paramStore = json.load(configFile)
        else:
            with open(self.configFile, 'w') as configFile:
                json.dump(self.paramStore, configFile, indent=4)

        self.storeMatchesJSON: bool = True

    # Set a custom config file name
    def setConfigFile(self, fileName: str) -> None:
        self.configFile = fileName
        
    # Update a single parameter in the store
    def setParam(self, key: str, value: Any) -> None:
        self.paramStore[key] = value
        self.storeMatchesJSON = False

    # Retrieve a single parameter from the store
    def getParam(self, key: str) -> Any:

        if key in self.paramStore:
            return self.paramStore[key]
        else:
            return None

    # Load and return all parameters from self
    def getParams(self) -> dict:
        return self.paramStore

    # Load and return all parameters from JSON file
    def getParamsFromJson(self) -> dict:
        with open(self.configFile, 'r') as configFile:
            return json.load(configFile)
    
    #return True if JSON file updated, false if no changes were made.
    def saveParamsToJson(self) -> bool:

        if self.storeMatchesJSON:
            return False
        
        with open(self.configFile, 'w') as configFile:
            json.dump(self.paramStore, configFile, indent=4)
            self.storeMatchesJSON = True
            return True

    # Load parameters from JSON file into paramStore
    def loadParamsFromJson(self) -> None:
        with open(self.configFile, 'r') as configFile:
            self.paramStore = json.load(configFile)
    
QueensCanyon: QC_Controller = QC_Controller('', '')
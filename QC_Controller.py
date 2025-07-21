
import json
import struct

class QC_Controller:
    def __init__(self, h2cStream: str, c2hStream: str):
        self.h2c_path: str = h2cStream
        self.c2h_path: str = c2hStream
        self.paramStore: dict = {}
        self.configFile = 'config.json'

    def setConfigFile(self, fileName: str) -> None:
        self.configFile = fileName
        
    def setParam(self, key: str, value: any) -> None:
        self.paramStore[key] = value

    def getParam(self, key: str) -> any:
        return self.paramStore[key]
    
    def saveParamsToJson(self, fileName: str = self.configFile) -> None:
        with open(fileName, 'w') as configFile:
            json.dump(self.paramStore, configFile, indent=4)

    def loadParamsFromJson(self, fileName: str) -> None:
        with open(fileName, 'r') as configFile:
            self.paramStore = json.load(configFile)

    def programParam(self, key: str) -> None:
        pass

    def programAllParams(self) -> None:
        pass
    
    
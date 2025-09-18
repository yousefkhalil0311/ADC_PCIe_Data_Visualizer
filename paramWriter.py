from enum import Enum, auto
import firebase_admin
from firebase_admin import credentials, db
from sseclient import SSEClient
import threading
import json
import requests
import os
import struct
import time

#global parameter store & hardware controller
from QC_Controller import QueensCanyon


#Enum to hold Params that will be reference in the application. Decouples app from config file and from the command stream output
class Params(Enum):

    # channel enable params
    CH0_EN = auto()
    CH1_EN = auto()
    CH2_EN = auto()
    CH3_EN = auto()
    CH4_EN = auto()
    CH5_EN = auto()
    CH6_EN = auto()
    CH7_EN = auto()

    # ddc enable params
    DDC0_EN = auto()
    DDC1_EN = auto()
    DDC2_EN = auto()

    # ddc control params
    DDC0_FMIX = auto()
    DDC0_SFOUT = auto()
    DDC1_FMIX = auto()
    DDC1_SFOUT = auto()
    DDC2_FMIX = auto()
    DDC2_SFOUT = auto()

    # filter params
    LP500MHZ_EN = auto()
    LP1GHZ_EN = auto()
    LP2GHZ_EN = auto()
    BYPASS_EN = auto()

    # attenuation params
    ATTENUATION_BVAL = auto()

    # system state params
    SYSTEM_EN = auto()
    CAL_EN = auto()

    # acquisition params
    ACQUIREBYSAMPLES = auto()
    ACQUIREBYTIME_MS = auto()
    ACQUISITIONTIME_MS = auto()
    NUMSAMPLES_CAPTURE = auto()

#class to store info about a parameter. desc=configFile name, val=value stored in configFile
class ParamInfo:
    def __init__(self, desc: Params, val: int):   
        self.desc: Params = desc
        self.val: int = val
     

# dictionary to map JSON config params to Params
PARAM_TABLE: dict[str, ParamInfo] = {
    "Channel 0-Enable":         ParamInfo(Params.CH0_EN,                0),
    "Channel 1-Enable":         ParamInfo(Params.CH1_EN,                0),
    "Channel 2-Enable":         ParamInfo(Params.CH2_EN,                0),
    "Channel 3-Enable":         ParamInfo(Params.CH3_EN,                0),
    "Channel 4-Enable":         ParamInfo(Params.CH4_EN,                0),
    "Channel 5-Enable":         ParamInfo(Params.CH5_EN,                0),
    "Channel 6-Enable":         ParamInfo(Params.CH6_EN,                0),
    "Channel 7-Enable":         ParamInfo(Params.CH7_EN,                0),
    "DDC 0-1":                  ParamInfo(Params.DDC0_EN,               0),
    "DDC 0-2":                  ParamInfo(Params.DDC1_EN,               0),
    "DDC 0-3":                  ParamInfo(Params.DDC2_EN,               0),
    "Fmix (MHz)-0":             ParamInfo(Params.DDC0_FMIX,             10),
    "Fmix (MHz)-1":             ParamInfo(Params.DDC0_SFOUT,            1),
    "Fmix (MHz)-2":             ParamInfo(Params.DDC1_FMIX,             1),
    "SFout (Msps)-0":           ParamInfo(Params.DDC1_SFOUT,            1),
    "SFout (Msps)-1":           ParamInfo(Params.DDC2_FMIX,             1),
    "SFout (Msps)-2":           ParamInfo(Params.DDC2_SFOUT,            1),
    "Select Path-500MHz LP":    ParamInfo(Params.LP500MHZ_EN,           1),
    "Select Path-1GHz LP":      ParamInfo(Params.LP1GHZ_EN,             0),
    "Select Path-2GHz LP":      ParamInfo(Params.LP2GHZ_EN,             0),
    "Select Path-Bypass":       ParamInfo(Params.BYPASS_EN,             0),
    "attenuation_binVal":       ParamInfo(Params.ATTENUATION_BVAL,      0),
    "System-Active":            ParamInfo(Params.SYSTEM_EN,             0),
    "Calibration Mode":         ParamInfo(Params.CAL_EN,                0),
    "Aquire by-num of Samples": ParamInfo(Params.ACQUIREBYSAMPLES,      0),
    "Aquire by-time(us)":       ParamInfo(Params.ACQUIREBYTIME_MS,      0),
    "aquisitionTime(ms)":       ParamInfo(Params.ACQUISITIONTIME_MS,    0),
    "num of Samples to get":    ParamInfo(Params.NUMSAMPLES_CAPTURE,    0)
}

QC_SCHEMA: dict[str, int] = {
		'startToken':        0xDEADBEEF,
        'startTokenAddr':    0x00,
		'statusAddr':        0x01,
		'schemaVersion':     0x01,
		'schemaVersionAddr': 0x02,
		'hostTimeAddr': 	 0x03,
		'deviceTime':        0x04,
		'numParamsAddr':     0x05,
		'endHeaderToken': 	 0xDEADBEEF,
		'endHeaderAddr': 	 0x06,
		'paramStartToken':   0xCCCCCCCC,
		'keyValSep':         0xBBBBBBBB,
		'paramEnd':          0xEEEEEEEE,
		'lastParam':         0xABABABAB,
		'endToken':          0xEEEEEEEE,
        'HOST_PARAM_CHANGE':   (1 << 31),
        'PARAM_CHANGE_ACK':    (1 << 30),
        'PARAM_CHANGE_DONE':   (1 << 29),
        'PARAM_CHANGE_STAT':   (1 << 28),
        'BRAM_SETUP_REQUEST':  (1 << 27),
        'HOST_SETUP_DONE':     (1 << 26),
        'BRAM_SCHEMA_RETURN':  (1 << 25),
        'BRAM_SCHEMA_VALID':   (1 << 24),
        'HOST_IND_OP_REQUEST': (1 << 23),
        'IND_OP_ACK':          (1 << 22),
        'IND_OP_ONLINE':       (1 << 21),
}

class paramWriter:

    def __init__(self, commandFilePath: str, configFilePath: str):
        
        self.commandFilePath = commandFilePath

        self.configFilePath = configFilePath

    #sets up BRAM upon request of the hardware
    def setupBRAM(self) -> bool:

        #check to see if the hardware is requesting for param data
        if True:# self.readPCIeBytes(QC_SCHEMA['statusAddr']) & QC_SCHEMA['BRAM_SETUP_REQUEST']:

            print('Initializing BRAM...')
            self.programBRAM()

            #set bram setup complete flag
            print('Setting BRAM complete flag...')
            status: int = self.readPCIeBytes(QC_SCHEMA['statusAddr'])

            status |= QC_SCHEMA['HOST_SETUP_DONE']

            self.writePCIeBytes(status, QC_SCHEMA['statusAddr'])

            #reset bram setup complete flag after 50ms delay
            time.sleep(50 / 1000)

            print('Resetting BRAM complete flag...')
            status: int = self.readPCIeBytes(QC_SCHEMA['statusAddr'])

            status &= ~QC_SCHEMA['HOST_SETUP_DONE']

            self.writePCIeBytes(status, QC_SCHEMA['statusAddr'])

            return True

        else:

            return False
    
    #programs the expected BRAM data given a dictionary mapping Params to config.json params
    def programBRAM(self) -> bool:

        version: int = self.readPCIeBytes(QC_SCHEMA['schemaVersionAddr'])

        #verify schema versions match between SW and HW
        '''
        if version != QC_SCHEMA['schemaVersion']:

            print('Hardware schema does not match software schema! Aborting...')

            return False
        '''

        #write start token
        self.writePCIeBytes(QC_SCHEMA['startToken'], QC_SCHEMA['startTokenAddr'])

        #write number of params to BRAM
        print(len(PARAM_TABLE.keys()), "this is the num of params")
        self.writePCIeBytes(len(PARAM_TABLE.keys()), QC_SCHEMA['numParamsAddr'])
        
        #write end header token
        self.writePCIeBytes(QC_SCHEMA['endHeaderToken'], QC_SCHEMA['endHeaderAddr'])

        #parameters begin
        address: int = QC_SCHEMA['endHeaderAddr'] + 1

        #write all params into BRAM
        for index, paramKey in enumerate(PARAM_TABLE.keys()):

            #param start
            self.writePCIeBytes(QC_SCHEMA['paramStartToken'], address)
            address += 1

            #store param id
            self.writePCIeBytes(index, address)
            address += 1

            paramName: str = PARAM_TABLE[paramKey].desc.name

            #store param key length
            self.writePCIeBytes(len(paramName), address)
            address += 1

            #store param key offset from current location
            self.writePCIeBytes(3, address)
            address += 1

            #param value
            self.writePCIeBytes(PARAM_TABLE[paramKey].val, address)
            address += 1

            #param key val separator
            self.writePCIeBytes(QC_SCHEMA['keyValSep'], address)
            address += 1

            #param key
            self.writePCIeString(paramName, address)
            address += (len(paramName) // 4) + 1

            #param end token
            self.writePCIeBytes(QC_SCHEMA['paramEnd'], address)
            address += 1

        
        #indicate end of params
        self.writePCIeBytes(QC_SCHEMA['lastParam'], address)
        address += 1

        #indicate end of bram content
        self.writePCIeBytes(QC_SCHEMA['endToken'], address)

        return True

    
    #set PARAM_TABLE to reflect the QC_Controller param store
    def setParamsTable(self):
        for key in PARAM_TABLE.keys():
            try:
                PARAM_TABLE[key].val = QueensCanyon.paramStore[key]
            except KeyError:
                print(f'Key {key} in PARAM_TABLE does not exist in the QC_Controller.')

    
    #set the file path for the file stream to write to BRAM content
    def setCommandStream(self, commandFilePath: str) -> None:
        
        self.commandFilePath = commandFilePath
    
    #set the file path for the json config file
    def setConfigFile(self, configFilePath: str) -> None:

        self.configFilePath = configFilePath

    #Write 32 bit value to file at offset
    def writePCIeBytes(self, data: int, offset: int) -> None:

        fd: int = os.open(self.commandFilePath, os.O_WRONLY)

        a: bytes = struct.pack('<I', data)

        os.pwrite(fd, a, offset * 4)

        os.close(fd)

    #Read 32 bit value from file at offset
    def readPCIeBytes(self, offset: int) -> int:

        fd: int = os.open(self.commandFilePath, os.O_RDONLY)

        data: bytes = os.pread(fd, 4, offset * 4)

        os.close(fd)

        return struct.unpack('<I', data)[0]

    #converts string to chunks of 32 bit values and writes to file at offset
    def writePCIeString(self, data: str, offset: int) -> None:

        chunks: list[str] = [data[index:index + 4] for index in range(0, len(data), 4)]

        for index, chunk in enumerate(chunks):

            bytesData: bytes = chunk.encode('ascii').ljust(4, b"\x00")

            dataToWrite: int = struct.unpack('<I', bytesData)[0]

            self.writePCIeBytes(dataToWrite, offset + index)

    #reads number of bytes from offset and returns the string values
    def readPCIeString(self, offset: int, numChars: int) -> str:

        if numChars == 0:
            return ''

        result: str = ""

        #1 address stores up to 4 chars, so number of address we read from = ceiling(numChars / 4)
        numWordsToRead = (numChars // 4) + 1

        for word in range(numWordsToRead):

            wordBytes: int = self.readPCIeBytes(offset + word)

            stringChunk: str = struct.pack('<I', wordBytes).decode('ascii')

            result += stringChunk

        return result

class databaseHandler:
    def __init__(self, serviceAccountKeyPath: str, databaseURL: str, databaseReference: str):

        #set params needed to connect to database
        self.path_to_serviceAccountKey: str = serviceAccountKeyPath
        self.databaseURL: str = databaseURL
        self.databaseReference: str = databaseReference

        #initialize FireBase Admin with service account
        cred = credentials.Certificate(self.path_to_serviceAccountKey)

        firebase_admin.initialize_app(cred, {
            "databaseURL": self.databaseURL
        })

        #get reference to database
        self.ref = db.reference(self.databaseReference)

        #flag set True to indicate whether database contents changed. Set false when change is handled
        self.databaseUpdatedFlag: bool = False

        #params for creating thread to listen for db changes
        self.listenerThread = None
        self.stopEvent = threading.Event()
    
    #Push an entry w/ autogenerated key to the Firebase Realtime Database.
    def pushData(self, data: dict) -> str | None:

        entry = self.ref.push(data)
        
        # Return the Firebase-generated unique key for this entry
        return entry.key
    
   #Set an entry w/ given key to the Firebase Realtime Database.
    def setData(self, data: dict) -> str | None:

        self.ref.set(data)


    #call passed callback function when event occurs
    def actOnEventListener(self, callback):

        reqURL: str = f"{self.databaseURL}/{self.databaseReference}.json"

        response = requests.get(reqURL, stream=True) #params= parameter for authentication
        client = SSEClient(reqURL)
        for event in client:
            if self.stopEvent.is_set():
                break
            if event.data.strip() == "null":
                continue
            data = json.loads(event.data)
            callback(event.event, data)


    #start listening for db changes on a background thread
    def listen(self, callback):

        #do nothing if already listening
        if self.listenerThread and self.listenerThread.is_alive():
            raise RuntimeError("Listener already running")
        
        self.stopEvent.clear()
        self.listenerThread = threading.Thread(target=self.actOnEventListener, args=(callback,), daemon=True)

        self.listenerThread.start()

    #stop listening for database changes
    def stopListening(self):

        self.stopEvent.set()

        if self.listenerThread:
            self.listenerThread.join()


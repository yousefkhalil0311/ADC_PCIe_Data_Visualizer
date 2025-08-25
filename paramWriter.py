from enum import Enum, auto

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
    desc: str
    val: int

#dictionary to map Params to JSON config params
PARAM_TABLE: dict[Params, ParamInfo] = {

    Params.CH0_EN:              ParamInfo("Channel 0-Enable", 0),
    Params.CH1_EN:              ParamInfo("Channel 1-Enable", 0),
    Params.CH2_EN:              ParamInfo("Channel 2-Enable", 0),
    Params.CH3_EN:              ParamInfo("Channel 3-Enable", 0),
    Params.CH4_EN:              ParamInfo("Channel 4-Enable", 0),
    Params.CH5_EN:              ParamInfo("Channel 5-Enable", 0),
    Params.CH6_EN:              ParamInfo("Channel 6-Enable", 0),
    Params.CH7_EN:              ParamInfo("Channel 7-Enable", 0),
    Params.DDC0_EN:             ParamInfo("DDC 0-1", 0),
    Params.DDC1_EN:             ParamInfo("DDC 0-2", 0),
    Params.DDC2_EN:             ParamInfo("DDC 0-3", 0),
    Params.DDC0_FMIX:           ParamInfo("Fmix (MHz)-0", 65),
    Params.DDC0_SFOUT:          ParamInfo("Fmix (MHz)-1", 100),
    Params.DDC1_FMIX:           ParamInfo("Fmix (MHz)-2", 135),
    Params.DDC1_SFOUT:          ParamInfo("SFout (Msps)-0", 0),
    Params.DDC2_FMIX:           ParamInfo("SFout (Msps)-1", 0),
    Params.DDC2_SFOUT:          ParamInfo("SFout (Msps)-2", 0),
    Params.LP500MHZ_EN:         ParamInfo("Select Path-500MHz LP", 0),
    Params.LP1GHZ_EN:           ParamInfo("Select Path-1GHz LP", 0),
    Params.LP2GHZ_EN:           ParamInfo("Select Path-2GHz LP", 0),
    Params.BYPASS_EN:           ParamInfo("Select Path-Bypass", 0),
    Params.ATTENUATION_BVAL:    ParamInfo("", 0),
    Params.SYSTEM_EN:           ParamInfo("System-Active", 0),
    Params.CAL_EN:              ParamInfo("Calibration Mode", 0),
    Params.ACQUIREBYSAMPLES:    ParamInfo("Aquire by-# of Samples", 0),
    Params.ACQUIREBYTIME_MS:    ParamInfo("Aquire by-time(us)", 0),
    Params.ACQUISITIONTIME_MS:  ParamInfo("aquisitionTime(ms)", 0),
    Params.NUMSAMPLES_CAPTURE:  ParamInfo("", 0)
    
}



class paramWriter:

    def __init__(self):
        
        return
    
    #generates the expected BRAM data given a dictionary mapping Params to config.json params
    def structureParams(self, paramaterTable: dict[Params, ParamInfo]) -> list[int]:
        return
    
    def setParamsFromJSON(self, configFile: str) -> None:
        return
    2
    def writeParamsToBRAM(self, commandStream: str) -> None:
        return
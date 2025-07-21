#class to handle aggregating parameter info to send to hardware system
class parameterStore:
    def __init__(self):
        
        #dictionary of default parameters
    self.paramStore: dict[str, any] = {

        'CH0_ENABLE': False,
        'DDC0_1_ENABLE': False,
        'DDC0_1_FMIX': 0,
        'DDC0_1_SAMPLERATE': 1,
        'DDC0_2_ENABLE': False,
        'DDC0_2_FMIX': 0,
        'DDC0_2_SAMPLERATE': 1,
        'DDC0_3_ENABLE': False,
        'DDC0_3_FMIX': 0,
        'DDC0_3_SAMPLERATE': 1,

        'CH1_ENABLE': False,
        'DDC1_1_ENABLE': False,
        'DDC1_1_FMIX': 0,
        'DDC1_1_SAMPLERATE': 1,
        'DDC1_2_ENABLE': False,
        'DDC1_2_FMIX': 0,
        'DDC1_2_SAMPLERATE': 1,
        'DDC1_3_ENABLE': False,
        'DDC1_3_FMIX': 0,
        'DDC1_3_SAMPLERATE': 1,

        'CH2_ENABLE': False,
        'DDC2_1_ENABLE': False,
        'DDC2_1_FMIX': 0,
        'DDC2_1_SAMPLERATE': 1,
        'DDC2_2_ENABLE': False,
        'DDC2_2_FMIX': 0,
        'DDC2_2_SAMPLERATE': 1,
        'DDC2_3_ENABLE': False,
        'DDC2_3_FMIX': 0,
        'DDC2_3_SAMPLERATE': 1,

        'CH3_ENABLE': False,
        'DDC3_1_ENABLE': False,
        'DDC3_1_FMIX': 0,
        'DDC3_1_SAMPLERATE': 1,
        'DDC3_2_ENABLE': False,
        'DDC3_2_FMIX': 0,
        'DDC3_2_SAMPLERATE': 1,
        'DDC3_3_ENABLE': False,
        'DDC3_3_FMIX': 0,
        'DDC3_3_SAMPLERATE': 1,

        'CH4_ENABLE': False,
        'DDC4_1_ENABLE': False,
        'DDC4_1_FMIX': 0,
        'DDC4_1_SAMPLERATE': 1,
        'DDC4_2_ENABLE': False,
        'DDC4_2_FMIX': 0,
        'DDC4_2_SAMPLERATE': 1,
        'DDC4_3_ENABLE': False,
        'DDC4_3_FMIX': 0,
        'DDC4_3_SAMPLERATE': 1,

        'CH5_ENABLE': False,
        'DDC5_1_ENABLE': False,
        'DDC5_1_FMIX': 0,
        'DDC5_1_SAMPLERATE': 1,
        'DDC5_2_ENABLE': False,
        'DDC5_2_FMIX': 0,
        'DDC5_2_SAMPLERATE': 1,
        'DDC5_3_ENABLE': False,
        'DDC5_3_FMIX': 0,
        'DDC5_3_SAMPLERATE': 1,

        'CH6_ENABLE': False,
        'DDC6_1_ENABLE': False,
        'DDC6_1_FMIX': 0,
        'DDC6_1_SAMPLERATE': 1,
        'DDC6_2_ENABLE': False,
        'DDC6_2_FMIX': 0,
        'DDC6_2_SAMPLERATE': 1,
        'DDC6_3_ENABLE': False,
        'DDC6_3_FMIX': 0,
        'DDC6_3_SAMPLERATE': 1,

        'CH7_ENABLE': False,
        'DDC7_1_ENABLE': False,
        'DDC7_1_FMIX': 0,
        'DDC7_1_SAMPLERATE': 1,
        'DDC7_2_ENABLE': False,
        'DDC7_2_FMIX': 0,
        'DDC7_2_SAMPLERATE': 1,
        'DDC7_3_ENABLE': False,
        'DDC7_3_FMIX': 0,
        'DDC7_3_SAMPLERATE': 1,
    }



    def setParam(self, key: str, value) -> None:
        self.paramStore[key] = value

    def getParam(self, key: str) -> any | None:
        self.paramStore[key]

    def saveParamsToFile(self, fileName: str) -> int:
        pass

    def loadParamsFromFile(self, fileName: str) -> int:
        pass

store: parameterStore = parameterStore()
import pyqtgraph as pg
from pyqtgraph.Qt import QtCore, QtGui, QtWidgets
from typing import Any, Union

#global parameter store & hardware controller
from QC_Controller import QueensCanyon

class LabelColumn:
    def __init__(self, layout: QtWidgets.QGridLayout, columnName: str,  columnIndex: int, *labels: str):

        self.labels: tuple[str, ...] = labels

        columnLabel: QtWidgets.QLabel = QtWidgets.QLabel(columnName)
        columnLabel.setMaximumSize(20, 100)

        layout.addWidget(columnLabel, 0, columnIndex)

        for i, label in enumerate(self.labels):

            label: QtWidgets.QLabel = QtWidgets.QLabel(columnName)
            label.setMaximumSize(20, 100)

            layout.addWidget(label, i + 1, columnIndex)

#Creates a column of checkboxes corresponding to the number of checkBocLabels arguments provided
class CheckBoxColumn:
    def __init__(self, layout: QtWidgets.QGridLayout, columnName: str, columnIndex: int, *checkBoxLabels: str):

        self.labels: tuple[str, ...] = checkBoxLabels
        self.columnName = columnName

        #store individual checkbox objects within column, as well as their current state
        self.checkBoxes: list[list[Union[QtWidgets.QCheckBox, int]]] = []

        #Create title for checkBox column
        columnLabel: QtWidgets.QLabel = QtWidgets.QLabel(columnName)
        columnLabel.setMaximumSize(len(columnName) * 8, 25)

        #add label to layout
        layout.addWidget(columnLabel, 0, columnIndex)

        #create 1 checkbox per label, store state upon change, add to layout
        for index, name in enumerate(self.labels):

            #create checkbox object
            self.checkBox: QtWidgets.QCheckBox = QtWidgets.QCheckBox(name)

            #add checkbox to column
            self.checkBoxes.append([self.checkBox, 0]) #0 corresponds to unchecked checkboxes; 2 is for checked boxes

            #if the checkbox is checked or unchecked, call the checkBoxCallback to store latest checkbox state
            self.checkBox.stateChanged.connect(lambda state, i = index: self.checkBoxCallback(i, state))
        
            #add to layout
            layout.addWidget(self.checkBox, index + 1, columnIndex)

    #callback to react to state changes on checkboxes
    def checkBoxCallback(self, index: int, state: int) -> None:
        self.checkBoxes[index][1] = state
        QueensCanyon.setParam(f"{self.columnName}-{self.labels[index]}", 1 if state else 0)

    #function to update widget data from paramStore
    def update(self) -> None:

        for index, checkBox in enumerate(self.checkBoxes):
            updatedState = QueensCanyon.getParam(f"{self.columnName}-{self.labels[index]}")

            #check to see if key exists
            if updatedState is None:
                return
            
            checkBox[0].setChecked(bool(updatedState))
            checkBox[1] = (updatedState * 2)

    #returns the states of all checkboxes in the column
    def getCheckBoxStates(self) -> list[int]:

        listofStates = []

        for _, state in self.checkBoxes:
            listofStates.append(state)
        
        return listofStates

#Creates a column of textBoxes corresponding to the numRows parameter
class LineEditColumn:
    def __init__(self, layout: QtWidgets.QGridLayout, columnName: str, columnIndex: int, numRows: int):

        self.name = columnName

        layout.addWidget(QtWidgets.QLabel(columnName), 0, columnIndex)

        #store individual textbox objects and the user text entered
        self.lineEdits: list[list[QtWidgets.QLineEdit, str]] = []

        #create 1 textBox row for the number of rows specified
        for rowNum in range(numRows):

            lineEdit: QtWidgets.QLineEdit = QtWidgets.QLineEdit()

            #store lineEdit and empty text
            self.lineEdits.append([lineEdit, ""])

            lineEdit.setMaximumSize(60, 20)

            #attach callback to automatically store text when entered
            lineEdit.editingFinished.connect(lambda rN = rowNum, le = lineEdit: self.storeTextCallback(rN, le.text()))

            #add lineEdit to column
            layout.addWidget(lineEdit, rowNum + 1, columnIndex)

    #callback to store user input
    def storeTextCallback(self, index: int, text: str) -> None:
        self.lineEdits[index][1] = text
        QueensCanyon.setParam(f"{self.name}-{index}", int(text))

    #function to update widget data from paramStore
    def update(self) -> None:

        for index, lineEdit in enumerate(self.lineEdits):
            updatedState = QueensCanyon.getParam(f"{self.name}-{index}")

            #check to see if key exists
            if updatedState is None:
                return
            
            lineEdit[0].setText(str(updatedState))
            lineEdit[1] = (str(updatedState))

    #get string entered in a single lineEdit box
    def getRowText(self, index: int) -> str:
        return self.lineEdits[index][1]
    
    def getAllText(self) -> list[str]:

        listOfStrings: list[str] = []

        for _, text in self.lineEdits:
            listOfStrings.append(text)

        return listOfStrings
    

#Creates a column of numRows dropDownBoxes with options corresponding to the checkBoxOptions parameters provided
class DropDownColumn:
    def __init__(self, layout: QtWidgets.QGridLayout, columnName: str, columnIndex: int, numRows: int, *checkBoxOptions: tuple[str, ...]):

        self.columnName = columnName
        self.columnIndex = columnIndex

        #add title of Column
        layout.addWidget(QtWidgets.QLabel(self.columnName), 0, self.columnIndex)

        #store instances of drop down boxes and the currently selected option
        self.dropDownBoxes: list[list[Union[QtWidgets.QComboBox, str]]] = []

        #create qty numRows drop down boxes, each having the options of checkBoxOptions 
        for rowNum in range(numRows):

            #create dropdown box object
            dropDownBox: QtWidgets.QComboBox = QtWidgets.QComboBox()

            #add options to dropdown box
            dropDownBox.addItems(checkBoxOptions)

            dropDownBox.setMaximumSize(60, 20)

            #store in class variable
            self.dropDownBoxes.append([dropDownBox, ""])

            #on change of option, calls dropDownCallback to set new Option
            dropDownBox.currentIndexChanged.connect(lambda optionString, index = rowNum: self.dropDownCallback(index, optionString))

            #add dropdown box to column
            layout.addWidget(dropDownBox, rowNum + 1, columnIndex)

    #callback used to store new option state when user selects a different option
    def dropDownCallback(self, index: int, optionString: str) -> None:
        self.dropDownBoxes[index][1] = optionString
        QueensCanyon.setParam(f"{self.columnName}-{index}", optionString)

    #function to update widget data from paramStore
    def update(self) -> None:

        for index, dropDown in enumerate(self.dropDownBoxes):
            updatedState = QueensCanyon.getParam(f"{self.columnName}-{index}")

            #check to see if key exists
            if updatedState is None:
                return
            
            dropDown[0].setCurrentIndex(updatedState)
            dropDown[1] = self.getDropDownOption(updatedState)

    #returns the selected option from 1 dropdown box
    def getDropDownOption(self, index: int) -> str:
        return self.dropDownBoxes[index][1]
    
    #returns state of all checkboxes in class object, or column
    def getAllDropDownStates(self) -> list[str]:

        listOfOptions: list[str] = []

        for _, optionString in self.dropDownBoxes:
            listOfOptions.append(optionString)

        return listOfOptions


class ChannelControlWidget:
    def __init__(self, channel: int, layout: QtWidgets.QBoxLayout):

        self.channel: int = channel

        self.GridLayout = QtWidgets.QGridLayout()
        layout.addLayout(self.GridLayout)

        #channel enable checkbox
        self.channelEnableCheck: CheckBoxColumn = CheckBoxColumn(self.GridLayout, f"Channel {self.channel}", 0, 'Enable')

        #Individual DDC enable checkboxes
        self.ddcCheckboxColumn: CheckBoxColumn = CheckBoxColumn(self.GridLayout, f"DDC {self.channel}", 1, '1', '2', '3')

        #DDC center frequency input column
        self.ddcFmixInputs: LineEditColumn = LineEditColumn(self.GridLayout, 'Fmix (MHz)', 2, 3)

        #DDC output sampling frequency column
        self.ddcSampleFreqOptions: DropDownColumn = DropDownColumn(self.GridLayout, 'SFout (Msps)', 3, 3, '1', '2.5', '5', '6.25', '7.8125', '10', '25', '62.5', '125', '250', '500', '1000')

    def getParamData(self) -> dict[str, list[Union[int, str]]]:
    
        return  {
            "chEnable": self.channelEnableCheck.getCheckBoxStates(),
            "ddcEnable": self.ddcCheckboxColumn.getCheckBoxStates(),
            "ddcFmixVals": self.ddcFmixInputs.getAllText(),
            "ddcFsampleVals": self.ddcSampleFreqOptions.getAllDropDownStates()
        }
    
    def update(self):
        self.channelEnableCheck.update()
        self.ddcCheckboxColumn.update()




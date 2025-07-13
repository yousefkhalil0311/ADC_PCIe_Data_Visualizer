import pyqtgraph as pg
from pyqtgraph.Qt import QtCore, QtGui, QtWidgets
from typing import Any, Union

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

    #returns the states of all checkboxes in the column
    def getCheckBoxStates(self) -> list[int]:

        listofStates = []

        for _, state in self.checkBoxes:
            listofStates.append(state)
        
        return listofStates

#Creates a column of textBoxes corresponding to the numRows parameter
class LineEditColumn:
    def __init__(self, layout: QtWidgets.QGridLayout, columnName: str, columnIndex: int, numRows: int):

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
            lineEdit.textChanged.connect(lambda text, index = rowNum: self.storeTextCallback(index, text))

            #add lineEdit to column
            layout.addWidget(lineEdit, rowNum + 1, columnIndex)

    #callback to store user input
    def storeTextCallback(self, index: int, text: str) -> None:
        self.lineEdits[index][1] = text

    #get string entered in a single lineEdit box
    def getRowText(self, index: int) -> str:
        return self.lineEdits[index][1]
    
    def getAllText(self) -> list[str]:

        listOfStrings: list[str] = []

        for _, text in self.lineEdits:
            listOfStrings.append(text)

        return listOfStrings

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
        LineEditColumn(self.GridLayout, 'SFout (MHz)', 3, 3)

    def getParamData(self) -> dict[str, list[Union[int, str]]]:
    
        return  {
            "chEnable": self.channelEnableCheck.getCheckBoxStates(),
            "ddcEnable": self.ddcCheckboxColumn.getCheckBoxStates(),
            "ddcFmixVals": self.ddcFmixInputs.getAllText()
        }




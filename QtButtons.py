import pyqtgraph as pg
from pyqtgraph.Qt import QtCore, QtGui, QtWidgets
from collections.abc import Callable

#global parameter store & hardware controller
from QC_Controller import QueensCanyon

#Class to instantiate a group of Radio Buttons that are exclusive to the given instantiation
class RadioButton:
    def __init__(self, title: str, layout: QtWidgets.QBoxLayout, *options: str, default: str | None = None):

        #Set Radio Button Set title and store options arguments
        self.title: str = title
        self.options: tuple[str, ...] = options

        #Create label for Radio Buttons
        self.label = QtWidgets.QLabel('Uninitialized Label')
        self.label.setText(f"{title}:")

        self.currentButton: str = default

        #Add label to layout
        layout.addWidget(self.label)

        #Create button group for Radio Buttons. Otherwise, different sets of Radio Buttons act as one set
        self.buttonGroup: QtWidgets.QButtonGroup = QtWidgets.QButtonGroup(layout)

        self.radioButtons: list[QtWidgets.QRadioButton] = []

        #Create list of Radio Buttons from the input list of option strings
        for radioButtonOption in options:

            radioButton: QtWidgets.QRadioButton = QtWidgets.QRadioButton(radioButtonOption)

            #Add Radio Buttons to the layout and to the button group
            self.radioButtons.append(radioButton)
            layout.addWidget(radioButton)
            self.buttonGroup.addButton(radioButton)
            
            #Preselect button set in the default parameter
            if radioButtonOption == default:
                radioButton.setChecked(True)


        #attach callback function to button group to handle state changes
        self.buttonGroup.buttonToggled.connect(self.setSelectedRadioButton)

    #callback to handle radio button state changes
    def setSelectedRadioButton(self, radioButton: QtWidgets.QRadioButton, checked: bool) -> None:

        #react when a button is selected
        if checked:
            QueensCanyon.setParam(f"{self.title}-{self.currentButton}", 0 if checked else 1)
            self.currentButton = radioButton.text()
            QueensCanyon.setParam(f"{self.title}-{self.currentButton}", 1 if checked else 0)

    def getSelectedRadioButton(self) -> str:
        return self.currentButton

    #function to update widget data from paramStore
    def update(self) -> None:

        for radioButton in self.radioButtons:

            updatedState = QueensCanyon.getParam(f"{self.title}-{radioButton.text()}")

            #check to see if key exists
            if updatedState is None:
                return
            
            radioButton.blockSignals(True)
            radioButton.setChecked(bool(updatedState))
            radioButton.blockSignals(False)

            self.currentButton = radioButton.text()

#Class to instantiate checkbox widgets in the parent layout
class CheckBox:
    def __init__(self, title: str, layout: QtWidgets.QVBoxLayout | QtWidgets.QHBoxLayout):

        self.title: str = title

        #Create label for checkbox
        self.label = QtWidgets.QLabel('Uninitialized Label')
        self.label.setText(f"{title}:")

        #Add label to layout
        layout.addWidget(self.label)

        #Create checkBox widget
        self.checkBox: QtWidgets.QCheckBox = QtWidgets.QCheckBox()

        self.isChecked: bool = False

        #function called when checkbox changes state
        self.checkBox.checkStateChanged.connect(self.checkStateCallback)
        
        #Add checkBox to parent layout
        layout.addWidget(self.checkBox)

    def checkStateCallback(self) -> None:
        self.isChecked = self.checkBox.isChecked()
        QueensCanyon.setParam(f"{self.title}", 1 if self.isChecked else 0)

    #function to update widget data from paramStore
    def update(self) -> None:

        updatedState = QueensCanyon.getParam(f"{self.title}")

        #check to see if key exists
        if updatedState is None:
            return
        
        self.checkBox.setChecked(bool(updatedState))

        self.isChecked = self.checkBox.isChecked()

    def getCheckState(self) -> bool:
        return self.checkBox.isChecked()

#Class to instantiate Pushbutton widgets in the parent layout
class PushButton:
    def __init__(self, title: str, layout: QtWidgets.QVBoxLayout | QtWidgets.QHBoxLayout, callback: Callable[[], None]):

        self.title: str = title

        self.pushButton = QtWidgets.QPushButton(self.title)

        layout.addWidget(self.pushButton)

        #pressing this button will call the callback function specified in the input parameters
        self.pushButton.clicked.connect(callback)


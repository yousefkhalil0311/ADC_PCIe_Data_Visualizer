import pyqtgraph as pg
from pyqtgraph.Qt import QtCore, QtGui, QtWidgets
from collections.abc import Callable

#Class to instantiate a group of Radio Buttons that are exclusive to the given instantiation
class RadioButton:
    def __init__(self, title: str, layout: QtWidgets.QBoxLayout, *options: str, default: str | None = None):

        #Set Radio Button Set title and store options arguments
        self.title: str = title
        self.options: tuple[str, ...] = options

        #Create label for Radio Buttons
        self.label = QtWidgets.QLabel('Uninitialized Label')
        self.label.setText(f"{title}:")

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

#Class to instantiate checkbox widgets in the parent layout
class CheckBox:
    def __init__(self, title: str, layout: QtWidgets.QVBoxLayout | QtWidgets.QHBoxLayout):

        self.title: str = title

        #Create label for Radio Buttons
        self.label = QtWidgets.QLabel('Uninitialized Label')
        self.label.setText(f"{title}:")

        #Add label to layout
        layout.addWidget(self.label)

        #Create checkBox widget
        self.checkBox: QtWidgets.QCheckBox = QtWidgets.QCheckBox()
        
        #Add checkBox to parent layout
        layout.addWidget(self.checkBox)

#Class to instantiate Pushbutton widgets in the parent layout
class PushButton:
    def __init__(self, title: str, layout: QtWidgets.QVBoxLayout | QtWidgets.QHBoxLayout, callback: Callable[[], None]):

        self.title: str = title

        self.pushButton = QtWidgets.QPushButton(self.title)

        layout.addWidget(self.pushButton)

        #pressing this button will call the callback function specified in the input parameters
        self.pushButton.clicked.connect(callback)


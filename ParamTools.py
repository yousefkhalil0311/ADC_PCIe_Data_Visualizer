import pyqtgraph as pg
from pyqtgraph.Qt import QtCore, QtGui, QtWidgets
from typing import Any

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

class CheckBoxColumn:
    def __init__(self, layout: QtWidgets.QGridLayout, columnName: str, columnIndex: int, *checkBoxLabels: str):

        self.labels: tuple[str, ...] = checkBoxLabels

        columnLabel: QtWidgets.QLabel = QtWidgets.QLabel(columnName)
        columnLabel.setMaximumSize(len(columnName) * 8, 25)

        layout.addWidget(columnLabel, 0, columnIndex)

        for index, name in enumerate(self.labels):

            checkBox: QtWidgets.QCheckBox = QtWidgets.QCheckBox(name)
        
            layout.addWidget(checkBox, index + 1, columnIndex)

class LineEditColumn:
    def __init__(self, layout: QtWidgets.QGridLayout, columnName: str, columnIndex: int, numRows: int):

        layout.addWidget(QtWidgets.QLabel(columnName), 0, columnIndex)

        for i in range(numRows):

            lineEdit: QtWidgets.QLineEdit = QtWidgets.QLineEdit()
            lineEdit.setMaximumSize(60, 20)

            layout.addWidget(lineEdit, i + 1, columnIndex)

class ChannelControlWidget:
    def __init__(self, channel: int, layout: QtWidgets.QBoxLayout):

        self.channel: int = channel

        self.GridLayout = QtWidgets.QGridLayout()
        layout.addLayout(self.GridLayout)

        CheckBoxColumn(self.GridLayout, f"Channel {self.channel}", 0, 'Enable')

        CheckBoxColumn(self.GridLayout, f"DDC {self.channel}", 1, '1', '2', '3')

        LineEditColumn(self.GridLayout, 'Fmix (MHz)', 2, 3)

        LineEditColumn(self.GridLayout, 'SFout (MHz)', 3, 3)




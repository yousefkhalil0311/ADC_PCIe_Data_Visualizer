import pyqtgraph as pg
from pyqtgraph.Qt import QtCore, QtGui, QtWidgets

class ParamTable:
    def __init__(self, layout: QtWidgets.QBoxLayout, *columns: str):

        self.columns: tuple[str, ...] = columns

        self.VerticalLayout = QtWidgets.QVBoxLayout()

        self.HorizontalLayout = QtWidgets.QHBoxLayout()

        for columnName in self.columns:

            newLabel = QtWidgets.QLabel(columnName)

            self.HorizontalLayout.addWidget(newLabel)


        self.VerticalLayout.addLayout(self.HorizontalLayout)

        layout.addLayout(self.VerticalLayout)

        
class ParamRow:
    def __init__(self, layout: QtWidgets.QBoxLayout, *rowContents: any):

        self.HorizontalLayout = QtWidgets.QHBoxLayout()
        
        self.rowContents: tuple[any, ...] = rowContents

        for entry in self.rowContents:
            self.HorizontalLayout.addWidget(entry)
        
        layout.addLayout(self.HorizontalLayout)


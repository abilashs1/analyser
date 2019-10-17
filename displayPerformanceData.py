'''
Created on Oct 12, 2019

@author: AbilashS2
'''
import csv

from PySide2.QtWidgets import QWidget, QTableView, QVBoxLayout
from PySide2.QtGui import QStandardItemModel, QStandardItem

class DisplayPerformanceData(QWidget):
    def __init__(self, parent=None):
        super(DisplayPerformanceData, self).__init__(parent)

        self.model = QStandardItemModel(self)

        self.tableView = QTableView(self)
        self.tableView.setModel(self.model)
        self.tableView.horizontalHeader().setStretchLastSection(True)

        self.layoutVertical = QVBoxLayout(self)
        self.layoutVertical.addWidget(self.tableView)

    def loadCsv(self, fileName):
        with open(fileName, "r") as fileInput:
            for row in csv.reader(fileInput):    
                items = [
                    QStandardItem(field)
                    for field in row
                ]
                self.model.appendRow(items)        
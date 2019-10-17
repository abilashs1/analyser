
#############################################################################
##
## Copyright (C) 2016 The Qt Company Ltd.
## Contact: http://www.qt.io/licensing/
##
## This file is part of the Qt for Python examples of the Qt Toolkit.
##
## $QT_BEGIN_LICENSE:BSD$
## You may use this file under the terms of the BSD license as follows:
##
## "Redistribution and use in source and binary forms, with or without
## modification, are permitted provided that the following conditions are
## met:
##   * Redistributions of source code must retain the above copyright
##     notice, this list of conditions and the following disclaimer.
##   * Redistributions in binary form must reproduce the above copyright
##     notice, this list of conditions and the following disclaimer in
##     the documentation and/or other materials provided with the
##     distribution.
##   * Neither the name of The Qt Company Ltd nor the names of its
##     contributors may be used to endorse or promote products derived
##     from this software without specific prior written permission.
##
##
## THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
## "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
## LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
## A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
## OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
## SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
## LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
## DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
## THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
## (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
## OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE."
##
## $QT_END_LICENSE$
##
#############################################################################

# PySide2 tutorial 4


import sys
from PySide2.QtCore import QObject, Signal, Slot, QThread, QFile, QIODevice, SIGNAL, SLOT, Qt   
from PySide2.QtWidgets import (QPushButton, QDialog, QTreeWidget, QLabel,
                             QTreeWidgetItem, QVBoxLayout, QLineEdit,
                             QHBoxLayout, QFrame, QComboBox, QGridLayout, 
                             QMessageBox, QFileDialog, QPlainTextEdit,
                             QApplication, QWidget, QScrollArea)

from PySide2.QtGui import (QPalette, QColor, QFont)

import os
from logFileParser import get_data_from_file, translate_data_to_json
from csvGenerator import base_log_path
from displayPerformanceData import DisplayPerformanceData
from iploader import load_vos_package_ip
from serialMonitor import SerialMonitorThread, get_available_serial_ports
from collapsible import CollapsibleWidget, get_verifone_color, get_white_color, get_white_color_text
from performancechart import get_performace_chart

logfile_path = os.path.join(base_log_path, 'log.txt')

    
class MyWidget(QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        self.thread = SerialMonitorThread()
        self.thread.dataReady.connect(self.get_data, Qt.QueuedConnection)
        self.thread.setTerminationEnabled(True)                                
        
        #Menu
        self.setPalette(get_verifone_color())
        
        collapsible = CollapsibleWidget()
        self.init_logging(collapsible)        
        
        self.init_download(collapsible)
        
        self.init_analyser(collapsible)
        

        collapsible.add_sections()     
        # Scroll Area
        self.createLoggingDisplayLabel()        
        self.scrollArea = QScrollArea()
        self.scrollArea.setBackgroundRole(QPalette.Dark)
        self.scrollArea.setWidget(self.text)
        self.scrollArea.setWidgetResizable(True)        
        
        hLayout = QHBoxLayout()
        #hLayout.addLayout(vLayout)
        hLayout.addWidget(collapsible)
        hLayout.addWidget(self.scrollArea)
        
        self.setLayout(hLayout)       

    def init_logging(self, collapsible):
                
        self.logger = QPushButton("Start Logging", self)
        self.logger.setFont(QFont("Times", 14, QFont.Bold))
        self.logger.clicked.connect(lambda:self.display_log_data())
        self.logger.setStyleSheet("background-color: white");
        
        #self.filterLayout = QtWidgets.QHBoxLayout()
        self.logFilterLabel = QLabel('Filter', self)
        self.logFilterLabel.setFont(QFont("Times", 14, QFont.Bold))
        self.logFilterLabel.setPalette(get_white_color_text())
        self.logFilterLabel.setFixedWidth(60) 
        self.logFilter = QLineEdit(self)
        self.logFilter.setPalette(get_white_color())
        self.logFilter.setStyleSheet("background-color: white")
        self.logFilter.setFixedWidth(200)
        #self.filterLayout.addWidget(self.logFilterLabel, QtCore.Qt.AlignLeft)        
        #self.filterLayout.addWidget(self.logFilter, QtCore.Qt.AlignLeft)
                
        self.serialList = QComboBox()
        ports = get_available_serial_ports()
        if (len(ports) == 1):
            self.serialList.addItem(ports[0])
            self.thread.set_comport(self.serialList.currentText())
        else :
            self.serialList.addItem("Select")
            for port in ports:
                self.serialList.addItem(port)
                
        self.serialList.currentIndexChanged.connect(lambda:self.set_serial_port())
        self.serialList.setStyleSheet("background-color: white")
        self.clear = QPushButton("Clear Log File", self)
        self.clear.setStyleSheet("background-color: white");
        self.clear.setFont(QFont("Times", 14, QFont.Bold))
        self.clear.clicked.connect(lambda:self.clear_data())

        widget = QFrame(collapsible.get_tree())
        widget.setPalette(get_verifone_color())
        title = "Logging"
        self.loggerGrid = QGridLayout(widget)
        self.loggerGrid.addWidget(self.logger, 0, 0, 1, 2)
        self.loggerGrid.addWidget(self.logFilterLabel, 1, 0, 1, 1)
        self.loggerGrid.addWidget(self.logFilter, 1, 1, 1, 1)
        self.loggerGrid.addWidget(self.serialList, 2, 0, 1, 2)
        self.loggerGrid.addWidget(self.clear, 3, 0, 1, 2)
        
        collapsible.include_section(title, widget)
    
    def init_download(self, collapsible):        
        self.download = QPushButton("Download Package", self)
        self.download.setFont(QFont("Times", 14, QFont.Bold))
        self.download.clicked.connect(lambda:self.send_file())
        self.download.setStyleSheet("background-color: white");        
        
        self.loadDownloadFile = QPushButton("Load File", self)
        self.loadDownloadFile.setFont(QFont("Times", 14, QFont.Bold))
        self.loadDownloadFile.clicked.connect(self.loadFromFile)
        self.loadDownloadFile.setStyleSheet("background-color: white");
        
        self.downloadFileName = QLineEdit("File name", self)            
        self.downloadFileName.setStyleSheet("background-color: white");
        self.downloadFileName.setFixedWidth(300)
        
        self.downloadAddress = QLineEdit("IP Address", self)            
        self.downloadAddress.setStyleSheet("background-color: white");
        self.downloadAddress.setFixedWidth(300)

        self.downloadStatus = QLabel("Download Status", self)            
        self.downloadStatus.setStyleSheet("background-color: rgba(3, 169, 229, 0); color : white");        
        self.downloadStatus.setFixedWidth(300)
        widget = QFrame(collapsible.get_tree())
        title = "Download"
        
        self.downloadGrid = QGridLayout(widget)
        self.downloadGrid.addWidget(self.download, 0, 0, 1, 2)
        self.downloadGrid.addWidget(self.loadDownloadFile, 1, 0, 1, 2)
        self.downloadGrid.addWidget(self.downloadFileName, 2, 0, 1, 2)
        self.downloadGrid.addWidget(self.downloadAddress, 3, 0, 1, 2)
        self.downloadGrid.addWidget(self.downloadStatus, 4, 0, 1, 2)   
        collapsible.include_section(title, widget)
        
    def init_analyser(self, collapsible):        
        self.performanceData = QPushButton("View Performance Data", self)
        self.performanceData.setFont(QFont("Times", 14, QFont.Bold))
        self.performanceData.clicked.connect(lambda:self.display_performance_data())
        self.performanceData.setStyleSheet("background-color: white");
        
        self.performanceChart = QPushButton("View Performance Chart", self)
        self.performanceChart.setFont(QFont("Times", 14, QFont.Bold))
        self.performanceChart.clicked.connect(lambda:self.display_performance_chart())
        self.performanceChart.setStyleSheet("background-color: white");
        
        widget = QFrame(collapsible.get_tree())
        title = "Analyser"        
        self.analyserGrid = QGridLayout(widget)
        self.analyserGrid.addWidget(self.performanceData, 0, 0, 1, 2)
        self.analyserGrid.addWidget(self.performanceChart, 1, 0, 1, 2)
        collapsible.include_section(title, widget)
        
    def loadFromFile(self):
        fileName,_ = QFileDialog.getOpenFileName(self,
                "Load Package", '',
                "Download Files (*.tgz);;All Files (*)")

        if not fileName:
            return

        try:
            in_file = open(str(fileName), 'rb')
        except IOError:
            QMessageBox.information(self, "Unable to open file",
                    "There was an error opening \"%s\"" % fileName)
            return
        in_file.close()
        self.downloadFileName.setText(fileName)        
            
    def createLoggingDisplayLabel(self):
        # Display Area  
        self.text = QPlainTextEdit(self)
        self.text.setReadOnly(True)
        self.text.setFont(QFont("Times", 12, QFont.Bold))
        self.text.setTextInteractionFlags(Qt.TextSelectableByMouse | Qt.TextSelectableByKeyboard)
        
    def clear_data(self):
        self.text.clear()
        os.remove(logfile_path, dir_fd=None)
    
    def display_log_data(self):
        #send_file()
        
        if ('COM' in self.serialList.currentText()):
            self.createLoggingDisplayLabel()
            self.scrollArea.setWidget(self.text)
            self.thread.stop()
            self.thread.start()
            
            data = get_data_from_file(logfile_path)
            if (len(data) > 0 and data != None):
                self.text.appendPlainText(data)
            self.logger.setDisabled(True)         
            
    def get_data(self, data):
        if (len(data) > 0):            
            logFile = open(logfile_path, "a")
            logFile.write(data)
            logFile.close()
            filterText = self.logFilter.text()
            if filterText in data.rstrip():
                self.text.appendPlainText(data.rstrip())
                vbar = self.scrollArea.verticalScrollBar()
                vbar.setValue(vbar.maximum())
        
    def display_performance_data(self):
        self.thread.stop()
        data = get_data_from_file(logfile_path)        
        jsonData = translate_data_to_json(data)        
        self.performanceData = DisplayPerformanceData()
        self.performanceData.loadCsv(os.path.join(base_log_path, "performance_data.csv"))
        self.scrollArea.setWidget(self.performanceData)
        self.logger.setDisabled(False)
    
    def display_performance_chart(self):
        self.thread.stop()        
        self.scrollArea.setWidget(get_performace_chart())
        self.logger.setDisabled(False)
        
    def set_serial_port(self):
        self.thread.set_comport(self.serialList.currentText())
     
    
    def send_file(self):        
        base_path = os.path.join("c:/", "VFI", 'wks', 'global-payment-application', 'GPA', 'output', 'vos2', 'gpa', 'dl.gpa-1.0.0.0-000.tgz')
        fileName = self.downloadFileName.text()
        try:
            in_file = open(str(fileName), 'rb')
        except IOError:
            QMessageBox.information(self, "Unable to open file",
                    "There was an error opening \"%s\"" % fileName)
            return
        in_file.close()
            
        load_vos_package_ip('192.168.0.104', fileName, self.downloadStatus)
    
if __name__ == '__main__':
    app = QApplication(sys.argv)
    
    widget = MyWidget()    
    widget.setWindowTitle('GPA Analyser 1.0.0')
    widget.show()
    sys.exit(app.exec_())


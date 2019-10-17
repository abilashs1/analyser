'''
Created on Oct 17, 2019

@author: AbilashS2
'''
import sys
import glob
from PySide2.QtCore import Signal, QThread
import serial

baud_rate = 115200 #whatever baudrate you are listening to
com_port1 = 'COM3' #replace with your first com port path
   
class SerialMonitorThread(QThread):
    dataReady = Signal(object)
    started=False
    listener = None
    port = None
    def slowly_produce_data(self):
        if (self.listener != None and self.listener.isOpen()):
            try :
                x = self.listener.readline()
            except :
                x = ''
            data = ''
            try :
                data = str(x, 'utf-8')
            except :
                if (len (x) > 0):
                    print ('Unknown Character: ', x)            
            components = []
            #print(x)
            if (len(components) == 0):
                return data
            for component in components:
                if component in data:            
                    return data;            
        return ''    
    
    def run(self):
        if (self.started == False and self.port != None and 'COM' in self.port):
            self.started = True
            if (self.listener == None or self.listener.isOpen() != True):
                self.listener = serial.Serial(self.port, baud_rate)
            while True:
                self.data = self.slowly_produce_data()
                # this will add a ref to self.data and avoid the destruction 
                if (len(self.data) > 0):
                    self.dataReady.emit(self.data)
                if (self.listener == None):
                    break
                    
    def stop(self):
        if (self.listener != None and self.listener.isOpen()):
            print ('Close')
            print ('terminate')
            self.terminate()
            self.listener.close()

            self.started = False
        
    def set_comport(self, port):
        self.port = port

def get_available_serial_ports():
    """ Lists serial port names

        :raises EnvironmentError:
            On unsupported or unknown platforms
        :returns:
            A list of the serial ports available on the system
    """
    if sys.platform.startswith('win'):
        ports = ['COM%s' % (i + 1) for i in range(256)]
    elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
        # this excludes your current terminal "/dev/tty"
        ports = glob.glob('/dev/tty[A-Za-z]*')
    elif sys.platform.startswith('darwin'):
        ports = glob.glob('/dev/tty.*')
    else:
        raise EnvironmentError('Unsupported platform')

    result = []
    for port in ports:
        try:
            s = serial.Serial(port)
            s.close()
            result.append(port)
        except (OSError, serial.SerialException):
            pass
    return result

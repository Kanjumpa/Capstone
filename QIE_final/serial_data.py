import queue
import threading
import datetime

import numpy as np
import serial

class SerialThread(threading.Thread):
    """ A thread for reading a serial port. The serial port
        is opened when the thread is started.
    
        data_q:
            Queue for received data. Items in the queue
            are (timestamp, data) pairs, where timestamp is the current time
            and date in iso format, data is a size(15) numpy array for 
            all single photon counts and conincidence counts

        error_q:
            Queue for error messages, including error when serial port
            fails to open

        port:
            String of the address of the serial port to open
        
        port_baud/stopbits/parity:
            Int, serial communication parameters

        NOTE:
            any subclass of threading.Thread should only override
            __init__() and run() and add attributes, according
            to Python standard library documentation.
    """ 
    def __init__(   self,
                    data_q,
                    error_q,
                    port_name, 
                    port_baud=19600,
                    port_stopbits=serial.STOPBITS_ONE,
                    port_parity=serial.PARITY_NONE):
        
        threading.Thread.__init__(self)

        self.serial_port = None;
        self.serial_arg = dict( port=port_name,
                                baudrate=port_baud,
                                stopbits=port_stopbits,
                                parity=port_parity)
        
        self.data_q = data_q
        self.error_q = error_q
        self.pause = False
        
        # threading.Event() is a flag which can be set to True by set(),
        # to false by clear(). Indicates if the thread should keep running
        self.alive = threading.Event()
        self.alive.set()
        
        
    def run(self):
        #try:
            # if there's a port already open, close it
        if self.serial_port:
            self.serial_port.close()
        
        # if any problem occur when opening the port,
        # save error message to error_q, exit  
        try:
            self.serial_port = serial.Serial('/dev/tty.wchusbserial1410')
            self.serial_port.baudrate = 19200
        except serial.SerialException as e:
            self.error_q.put(e)
            print("serial error")
            return
        
        while self.alive.isSet():
            if self.pause:
                continue
            # look for a high byte which signals start of data stream
            start_byte = self.serial_port.read(1)
            start_int = int(start_byte.hex(), 16)
            if(start_int != 255):
                continue
            else:
                # read data bytes in A,B,C,D,Count order
                # A, B, C, D are each 5 bytes
                # Count is 55 bytes
                data_out = self.serial_port.read(75)
                
                #record timestamp
                time_string = datetime.datetime.now().strftime("%H:%M:%S.%f")
                
                # initialize int to store data
                data_int = np.zeros(15)
                
                for i in range(15):
                    for j in range(5):
                        data_int[i] += data_out[i*5+j]*128**j
                self.data_q.put((time_string, data_int))
        
        # clean up
        if self.serial_port:
            self.serial_port.close()

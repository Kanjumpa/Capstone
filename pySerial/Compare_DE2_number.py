##########
#
#   Python script to read data from QIE DE2 board and print
#   for exact comparison with LabVIEW interface of ABCD

#   update period = 1s (= 10 UART transmission)
#   print all nine possible combination of 10 UART datapoint,
#   such that at least one of them will be in sync with LabVIEW

#   Data format and ordering:
#   A_out, B_out, C_out, D_out: each 32 bits, sent over 5 bytes,
#   each byte sending 7 bits
#   (except the last byte which sends 4 bits with a b'000' padding)
#   bauderate: 19200

#   each byte:
#   7 databit + 1 '0' termination bit
#   1 stop bit
#
#   an 8-bit b'11111111' termination byte between Count_out and A_out
#
#   NOTE: Python3 ONLY because of dependence on bytes type to convert to int
#   To work in Python2, needs to parse string manually to convert to int

#   Author: Qianshu Lu
#   Date: Nov. 3, 2016

import serial
import time
import numpy as np

update_num = 10; # UART in each datapoint
termination_num = 300 # number of data points
counter = 1; # counter for number of UART


termination_counter = 0;

# list to store all nine truncations of UARTs
A_data = np.zeros(10)
A_print = np.zeros(10)

# counter for each truncation
counter = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]


#ser = serial.Serial('/dev/tty.wchusbserial1410')
#ser.baudrate = 19200
#print('check port is open: ', ser.is_open)
#print('ser: ', ser)

record = np.array([])
record_int = np.array([])
while True:
    #start_byte = ser.read(1)
    #start_int = int(start_byte.hex(), 16)
    # look for the high byte, which signals start of data stream
    #if(start_int != 255):
    #    continue
    #else:
        # read data bytes
        #A_out = ser.read(5)
        #B_out = ser.read(5)
        #C_out = ser.read(5)
        #D_out = ser.read(5)
        #Count_out = ser.read(55)
        A_out = np.random.randint(10,size=5)
        record = np.concatenate((record, A_out))
        A_int = 0
        # move data to print if counter is 10 
        for j in range(5):
            A_int += A_out[j]#*128**j
        record_int = np.append(record_int, A_int)
        for i in range(10):
            if(counter[i] < 10):
                A_data[i] += A_int
                #print("data[i]: ", A_data[i])
            elif(counter[i] == 10):
                A_print[i] = A_data[i]
                #print("print[i]: ", A_print[i])
                A_data[i] = A_int
                counter[i] = 0
                if(i==0):
                    print(A_print)
                    print("record: ", record)
                    print("record int: ", record_int)
                    A_print = np.zeros(10)
                    print("")
        # update counter
        for i in range(10):
           counter[i] += 1 
        

##########
#
#   Python script to continuous read from serial port and print,
#   assuming the data is 18-bit binary, transmitted with UART configuration:
#   bauderate: 9600
#   7 databit + 1 '0' termination bit
#   1 stop bit
#
#   NOTE: Python3 ONLY because of dependence on bytes type to convert to int
#   To work in Python2, needs to parse string manually to convert to int
#   
#   Author: Qianshu Lu
#   Date: Oct. 15, 2016

#!/usr/bin/env python3

import serial
import time

ser = serial.Serial('/dev/tty.wchusbserial1410')
print('check port is open: ', ser.is_open)
print('ser: ', ser)

line = []
i = 0
while True:
    some_bytes = ser.read(3)
    byte1 = some_bytes[:1];
    byte2 = some_bytes[1:2];
    byte3 = some_bytes[2:3];
    print("all bytes: ", some_bytes)
    print("byte1: ", byte1)
    print("byte2: ", byte2)
    print("byte3: ", byte3)

    int1 = int(byte1.hex(), 16)
    int2 = int(byte2.hex(), 16)*128
    int3 = int(byte3.hex(), 16)*128*128

    print("number: ", int1+int2+int3)

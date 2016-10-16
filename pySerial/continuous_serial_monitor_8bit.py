##########
#
#   Python script to continuous read from serial port and print,
#   assuming data is 8-bit, trasnmitted by UART configuration
#   baudrate: 9600
#   8 data bit, 1 stop bit
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
    some_bytes = ser.read(1)
    temp = int(some_bytes.hex(), 16)
    if temp != i:
        i = temp
        print('number:', i)

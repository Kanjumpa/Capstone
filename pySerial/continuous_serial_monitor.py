from __future__ import print_function
import serial
import time

ser = serial.Serial()
ser.baudrate = 9600
ser.port='COM3'
ser.open()
print('check port is open: ', ser.is_open)
print('ser: ', ser)

line = []
while True:
	some_bytes = ser.read(1)
	i = int.from_bytes(some_bytes, byteorder='big')
	print('number:', i)
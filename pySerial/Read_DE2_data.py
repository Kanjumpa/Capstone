##########
#
#   Python script to read data from QIE DE2 board.
#   Data format and ordering:
#   A_out, B_out, C_out, D_out: each 32 bits, sent over 5 bytes,
#   each byte sending 7 bits
#   (except the last byte which sends 4 bits with a b'000' padding)
#   Count_out: 352 bits, send over the same 5-byte pattern (32 bits) * 11 times
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
#   Date: Oct. 22, 2016

import serial
import time

ser = serial.Serial('/dev/tty.wchusbserial1410')
ser.baudrate = 19200
print('check port is open: ', ser.is_open)
print('ser: ', ser)

line = []
i = 0
while True:
    start_byte = ser.read(1)
    start_int = int(start_byte.hex(), 16)
    # print("start_byte is: ", start_byte)
    # print("start int is: ", start_int)

    # look for the high byte, which signals start of data stream
    if(start_int != 255):
        continue
    else:
        # read data bytes
        A_out = ser.read(5)
        B_out = ser.read(5)
        C_out = ser.read(5)
        D_out = ser.read(5)
        Count_out = ser.read(55)

        # for 5-byte data, each byte has 7 bits, except 4 for the last
        # printing order is opposite to reading order
        # (DE2 sends LSB first)
        print("A_out binary: ", '{0:04b}'.format(A_out[4]),
              '{0:07b}'.format(A_out[3]), '{0:07b}'.format(A_out[2]),
              '{0:07b}'.format(A_out[1]), '{0:07b}'.format(A_out[0]))
        print("B_out binary: ", '{0:04b}'.format(B_out[4]),
              '{0:07b}'.format(B_out[3]), '{0:07b}'.format(B_out[2]),
              '{0:07b}'.format(B_out[1]), '{0:07b}'.format(B_out[0]))
        print("C_out binary: ", '{0:04b}'.format(C_out[4]),
              '{0:07b}'.format(C_out[3]), '{0:07b}'.format(C_out[2]),
              '{0:07b}'.format(C_out[1]), '{0:07b}'.format(C_out[0]))
        print("D_out binary: ", '{0:04b}'.format(D_out[4]),
              '{0:07b}'.format(D_out[3]), '{0:07b}'.format(D_out[2]),
              '{0:07b}'.format(D_out[1]), '{0:07b}'.format(D_out[0]))

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

ser = serial.Serial('/dev/tty.wchusbserial1410')
ser.baudrate = 19200
print('check port is open: ', ser.is_open)
print('ser: ', ser)
while True:
    start_byte = ser.read(1)
    start_int = int(start_byte.hex(), 16)
    #print("start_byte is: ", start_byte)
    #print("start int is: ", start_int)

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

        command = input()
        # print("command is: ", command)
        if(command == '0'):
            exit()
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
        print("Count_out binary (first 11 bytes):  ", '{0:07b}'.format(Count_out[10]),
              '{0:04b}'.format(Count_out[9]), '{0:07b}'.format(Count_out[8]),
              '{0:07b}'.format(Count_out[7]), '{0:07b}'.format(Count_out[6]),
              '{0:07b}'.format(Count_out[5]), '{0:04b}'.format(Count_out[4]),
              '{0:07b}'.format(Count_out[3]), '{0:07b}'.format(Count_out[2]),
              '{0:07b}'.format(Count_out[1]), '{0:07b}'.format(Count_out[0]))
        print("Count_out binary (second 11 bytes): ", '{0:07b}'.format(Count_out[21]),
              '{0:07b}'.format(Count_out[20]), '{0:04b}'.format(Count_out[19]),
              '{0:07b}'.format(Count_out[18]), '{0:07b}'.format(Count_out[17]),
              '{0:07b}'.format(Count_out[16]), '{0:07b}'.format(Count_out[15]),
              '{0:04b}'.format(Count_out[14]), '{0:07b}'.format(Count_out[13]),
              '{0:07b}'.format(Count_out[12]), '{0:07b}'.format(Count_out[11]))
        print("Count_out binary (third 11 bytes):  ", '{0:07b}'.format(Count_out[32]),
              '{0:07b}'.format(Count_out[31]), '{0:07b}'.format(Count_out[30]),
              '{0:04b}'.format(Count_out[29]), '{0:07b}'.format(Count_out[28]),
              '{0:07b}'.format(Count_out[27]), '{0:07b}'.format(Count_out[26]),
              '{0:07b}'.format(Count_out[25]), '{0:04b}'.format(Count_out[24]),
              '{0:07b}'.format(Count_out[23]), '{0:07b}'.format(Count_out[22]))
        print("Count_out binary (fourth 11 bytes): ", '{0:07b}'.format(Count_out[43]),
              '{0:07b}'.format(Count_out[42]), '{0:07b}'.format(Count_out[41]),
              '{0:07b}'.format(Count_out[40]), '{0:04b}'.format(Count_out[39]),
              '{0:07b}'.format(Count_out[38]), '{0:07b}'.format(Count_out[37]),
              '{0:07b}'.format(Count_out[36]), '{0:07b}'.format(Count_out[35]),
              '{0:04b}'.format(Count_out[34]), '{0:07b}'.format(Count_out[33]))
        print("Count_out binary (fifth 11 bytes):  ", '{0:04b}'.format(Count_out[54]),
              '{0:07b}'.format(Count_out[53]), '{0:07b}'.format(Count_out[52]),
              '{0:07b}'.format(Count_out[51]), '{0:07b}'.format(Count_out[50]),
              '{0:04b}'.format(Count_out[49]), '{0:07b}'.format(Count_out[48]),
              '{0:07b}'.format(Count_out[47]), '{0:07b}'.format(Count_out[46]),
              '{0:07b}'.format(Count_out[45]), '{0:04b}'.format(Count_out[44]))

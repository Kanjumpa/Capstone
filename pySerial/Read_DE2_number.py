##########
#
#   Python script to read data from QIE DE2 board and print
#   (Count_out is not printed since it's too large: 352 bits)

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
#   Date: Oct. 24, 2016

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

        #command = input()
        # print("command is: ", command)
        #if(command == '0'):
        #    exit()
        # for 5-byte data, each byte has 7 bits, except 4 for the last
        # printing order is opposite to reading order
        # (DE2 sends LSB first)
        A_int = 0;
        B_int = 0;
        C_int = 0;
        D_int = 0;
        Count_int = 0;
        for i in range(5):
            A_int += A_out[i]*128**i
            B_int += B_out[i]*128**i
            C_int += C_out[i]*128**i
            D_int += D_out[i]*128**i
        print("A_out int: ", A_int)
        #print("B_out int: ", B_int)
        #print("C_out int: ", C_int)
        #print("D_out int: ", D_int)

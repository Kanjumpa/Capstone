##########
#
#   Python script to read data from QIE DE2 board and save to txt
#   (Count_out is not printed since it's too large: 352 bits)

#   Can specify different "update period", i.e. how many UART
#   transmission (0.1 second each) per data point.

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
#   Date: Oct. 27, 2016

import serial
import time

update_num = 20; # UART in each datapoint
termination_num = 300 # number of data points
counter = 1; # counter for number of UART


termination_counter = 0;

A_data = []
B_data = []
C_data = []
D_data = []

A_int = 0;
B_int = 0;
C_int = 0;
D_int = 0;

ser = serial.Serial('/dev/tty.wchusbserial1410')
ser.baudrate = 19200
print('check port is open: ', ser.is_open)
print('ser: ', ser)

command = input("start?")
while True:
    start_byte = ser.read(1)
    start_int = int(start_byte.hex(), 16)
    # look for the high byte, which signals start of data stream
    if(start_int != 255):
        continue
    else:
        # read data bytes
        A_out = ser.read(5)
        B_out = ser.read(5)
        C_out = ser.read(5)
        D_out = ser.read(5)
        #Count_out = ser.read(55)

        # for 5-byte data, each byte has 7 bits, except 4 for the last
        # printing order is opposite to reading order
        # (DE2 sends LSB first)
        
        if(counter == update_num):
            print("A_out int: ", A_int)
            print("B_out int: ", B_int)
            print("C_out int: ", C_int)
            print("D_out int: ", D_int)
            print("")
            A_data.append(A_int)
            B_data.append(B_int)
            C_data.append(C_int)
            D_data.append(D_int)
            A_int = 0
            B_int = 0
            C_int = 0
            D_int = 0
            counter = 0;
            termination_counter += 1

        for i in range(5):
            A_int += A_out[i]*128**i
            B_int += B_out[i]*128**i
            C_int += C_out[i]*128**i
            D_int += D_out[i]*128**i

        counter += 1;
           
        # data taking is done, print and save to file
        if(termination_counter == termination_num):
            time = time.strftime("%Y%m%d_%H%M%S")
            f = open("ABCD_"+time+".txt", 'w');
            f.write("################################\n")
            f.write("# Generated by: Save_DE2_number.py\n")
            f.write("\n")
            f.write("# Generated on: "+time+"\n")
            f.write("\n")
            f.write("# update period: " + repr(update_num*0.1)+"\n")
            f.write("# number of data points: " + repr(termination_num)+"\n");
            f.write("\n")
            f.write("#A_data, B_data, C_data, D_data\n")
            for i in range(termination_num):
                f.write(repr(A_data[i])+"   "+repr(B_data[i])+
                        "   "+repr(C_data[i])+"   "+repr(D_data[i])+"\n")
            print("A_data: ", A_data)
            print("")
            print("B_data: ", B_data)
            print("")
            print("C_data: ", C_data)
            print("")
            print("D_data: ", D_data)
            print("")
            exit()

        

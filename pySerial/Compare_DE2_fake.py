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

import numpy as np

update_num = 10; # UART in each datapoint
termination_num = 300 # number of data points
counter = 1; # counter for number of UART


termination_counter = 0;

# list to store all nine truncations of UARTs
A_data = np.zeros(10)
A_print = np.zeros(10)

# counter for each truncation
counter = [9,8,7,6,5,4,3,2,1,0]



record = np.array([])
record_int = np.array([])
A_out = np.array([1,1,2,1,1,1,1,1,1,1,  1,1,1,1,1,1,1,1,1,1, 1,1,1,1,1,1,1,1,1,1, 1,1,1,1,1,1,1,1,1,11,  1,1,1,1,1,1,1,1,1,1,1,1,  1,1,1,1,1,1,1,1,1,1,  1,1,1,1,1,1,1,1,1,1,  1,1,1,1,1,1,1,1,1,1,1,  1,1,1,1,1,1,1,1,1,1,  1,1,1,1,1,1,1,1,1,1,1])
for s in range(40):
        A_int = 0
        for j in range(2):
            A_int += A_out[2*s+j]
        # move data to print if counter is 10 
        for i in range(10):
            # add int to data array if counter not 10
            if(counter[i] < 10):
                A_data[i] += A_int
                #print("data[i]: ", A_data[i])  
            # move data to print array if counter is 10
            # and clear data
            elif(counter[i] == 10):
                A_print[i] = A_data[i]
                #print("print[i]: ", A_print[i])
                A_data[i] = A_int
                counter[i] = 0
                # when 0th counter is 10, print array should be filled,
                # print and clear print array
                if(i==9):
                    print(A_print)
                    A_print = np.zeros(10)
        # update counter
        for i in range(10):
           counter[i] += 1 
        

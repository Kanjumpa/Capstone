#!/usr/bin/env python3

import serial_data
import time
import queue
import numpy as np
from utils import get_item_from_queue


def main():
        data_q = queue.Queue()
        error_q = queue.Queue()
        portname = '/dev/tty.wchusbserial1410'
        
        serial_monitor = serial_data.SerialThread(
                data_q,
                error_q,
                portname)
                
        serial_monitor.start()
        
        serial_error = get_item_from_queue(error_q)
        if serial_error is not None:
            serial_monitor = None
            print("serial error")
            return
       
        print("thread started without error") 
        serial_active = True
        update_period = 1
        print("update period is ", update_period)
        while True:
            print("thread alive: ", serial_monitor.is_alive())
            time.sleep(1)
            data = get_item_from_queue(data_q)
            for i in range(9):
                data += get_item_from_queue(data_q)
            print(data)
    
if __name__ == '__main__':
    main()

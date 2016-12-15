#!/usr/bin/env python3

from PyQt4 import QtGui, QtCore

import sys
import serial_data
import queue
import numpy as np
import datetime
import csv
import argparse
import time

from Skeleton import GuiSkeleton


class QIE_Gui(GuiSkeleton):
    """ 
        Class that manages backend functions of the GUI parts.
        Comments are made extensive for first-time PyQt4 and Thread module users.
    """
   
    def __init__(self, portname='/dev/tty.wchusbserial1410'):
        
        # Initialize the GUI: create all the GUI parts and layouts
        super(QIE_Gui, self).__init__()
        
        self.data_q = None
        self.error_q = None
        self.timer = QtCore.QTimer()
        self.record_timer = QtCore.QTimer()
        self.serial_monitor = None
        self.record_active = False
        self.portname = portname
        
        # Connect actions on GUI to custon methods.
        # "clicked()": when a button is clicked.
        # "valueChanged(double)": when a double spinbox value has changed.
        QtCore.QObject.connect(self.quit_button, QtCore.SIGNAL("clicked()"), self.on_quit)
        QtCore.QObject.connect(self.start_button, QtCore.SIGNAL("clicked()"), self.on_start)
        QtCore.QObject.connect(self.stop_button, QtCore.SIGNAL("clicked()"), self.on_stop)
        QtCore.QObject.connect(self.update_spin, QtCore.SIGNAL("valueChanged(double)"), self.on_update_spinbox_change)
        QtCore.QObject.connect(self.record_button, QtCore.SIGNAL("clicked()"), self.on_record)
        
    def on_start(self):
        """ Start the data collection serial thread and update timer """
        
        if self.serial_monitor == None:
            print("creating new serial monitor")
            # Create Queue to store data and error messages from serial port
            self.data_q = queue.Queue()
            self.error_q = queue.Queue()
        
            # Create serial monitor thread
            self.serial_monitor = serial_data.SerialThread(
                    self.data_q,
                    self.error_q,
                    self.portname)
        
            # Start serial monitor thread (data collection will start running
            # in parallel to GUI monitor)
            self.serial_monitor.start()
        
            # See if any error occured when opening the serial port
            serial_error = self.get_item_from_queue(self.error_q)
            if serial_error != None:
                if serial_error == "serial error":
                    QtGui.QMessageBox.critical(self, 'SerialThread error', 
                           'Error when connecting to DE2; \nPlease turn on DE2 before collecting data.')
                self.serial_monitor = None
                return
        else:
            self.serial_monitor.pause = False
        
        # Get coincidence time window
        self.time_window = self.coincidence_spin.value()
        # Get update period from spinbox (default = 0.1)
        self.update_period = self.update_spin.value()
        # Connect timer trigger to on_timer method
        self.connect(self.timer, QtCore.SIGNAL('timeout()'), self.on_update_timer)
        # Set timer to update period (in milliseconds)
        self.timer.start(self.update_period*1000.0)

    
    def on_update_timer(self):
        """ Executed periodically when the serial update timer is fired 
        """
        # print("GUI:on_timer::update_period is ", self.update_period)
        
        # get number of data points = update_period / 0.1
        update_num = int(round(self.update_period/0.1))
        # print("GUI:on_timer::update_num is ", update_num)
        
        # Retrive data from Queue
        # Each qdata is a pair (time, num_data),
        # where num_data is a size(15) array containing all photon counts
        qdata = None
        while qdata is None:
            #print('in loop')
            qdata = self.get_item_from_queue(self.data_q)
        time = qdata[0]
        num_data = qdata[1]
        for i in range(update_num-1):
            qdata = self.get_item_from_queue(self.data_q)
            while qdata is None:
                #print('in second loop')
                qdata = self.get_item_from_queue(self.data_q)
            num_data += qdata[1]
        
        # Calculate statistical corrections.
        # Retrieve coincidence timewindow
        
        time_factor = self.time_window*10**(-9)/self.update_period
        raw_A = num_data[0]
        raw_B = num_data[1]
        raw_C = num_data[2]
        raw_D = num_data[3]

        stat_AB = raw_A*raw_B*time_factor
        stat_AC = raw_A*raw_C*time_factor
        stat_AD = raw_A*raw_D*time_factor
        stat_BC = raw_B*raw_C*time_factor
        stat_BD = raw_B*raw_D*time_factor
        stat_CD = raw_D*raw_D*time_factor
        stat_ABC = stat_AB*raw_C*time_factor
        stat_BCD = stat_BC*raw_D*time_factor
        stat_ABD = stat_AB*raw_D*time_factor
        stat_ACD = stat_AC*raw_D*time_factor
        stat_ABCD = stat_ABC*raw_D*time_factor
        
        self.A_display.setText("{:.0f}".format(num_data[0]))
        self.B_display.setText("{:.0f}".format(num_data[1]))
        self.C_display.setText("{:.0f}".format(num_data[2]))
        self.D_display.setText("{:.0f}".format(num_data[3]))
        self.AB_raw_display.setText("{:.0f}".format(num_data[4]))
        self.AC_raw_display.setText("{:.0f}".format(num_data[5]))
        self.AD_raw_display.setText("{:.0f}".format(num_data[6]))
        self.BC_raw_display.setText("{:.0f}".format(num_data[7]))
        self.BD_raw_display.setText("{:.0f}".format(num_data[8]))
        self.CD_raw_display.setText("{:.0f}".format(num_data[9]))
        self.ABC_raw_display.setText("{:.0f}".format(num_data[10]))
        self.BCD_raw_display.setText("{:.0f}".format(num_data[11]))
        self.ABD_raw_display.setText("{:.0f}".format(num_data[12]))
        self.ACD_raw_display.setText("{:.0f}".format(num_data[13]))
        self.ABCD_raw_display.setText("{:.0f}".format(num_data[14]))
        
        self.AB_stat_display.setText("{:.2E}".format(stat_AB))
        self.AC_stat_display.setText("{:.2E}".format(stat_AC))
        self.AD_stat_display.setText("{:.2E}".format(stat_AD))
        self.BC_stat_display.setText("{:.2E}".format(stat_BC))
        self.BD_stat_display.setText("{:.2E}".format(stat_BD))
        self.CD_stat_display.setText("{:.2E}".format(stat_CD))
        self.ABC_stat_display.setText("{:.2E}".format(stat_ABC))
        self.BCD_stat_display.setText("{:.2E}".format(stat_BCD))
        self.ABD_stat_display.setText("{:.2E}".format(stat_ABD))
        self.ACD_stat_display.setText("{:.2E}".format(stat_ACD))
        self.ABCD_stat_display.setText("{:.2E}".format(stat_ABCD))
        
        self.AB_corrected_display.setText("{:.2E}".format(num_data[4]-stat_AB))
        self.AC_corrected_display.setText("{:.2E}".format(num_data[5]-stat_AC))
        self.AD_corrected_display.setText("{:.2E}".format(num_data[6]-stat_AD))
        self.BC_corrected_display.setText("{:.2E}".format(num_data[7]-stat_BC))
        self.BD_corrected_display.setText("{:.2E}".format(num_data[8]-stat_BD))
        self.CD_corrected_display.setText("{:.2E}".format(num_data[9]-stat_CD))
        self.ABC_corrected_display.setText("{:.2E}".format(num_data[10]-stat_ABC))
        self.BCD_corrected_display.setText("{:.2E}".format(num_data[11]-stat_BCD))
        self.ABD_corrected_display.setText("{:.2E}".format(num_data[12]-stat_ABD))
        self.ACD_corrected_display.setText("{:.2E}".format(num_data[13]-stat_ACD))
        self.ABCD_corrected_display.setText("{:.2E}".format(num_data[14]-stat_ABCD))
        
        # Check if data recording is active
        if self.record_active:
            # if this is the first data to record, start record_timer
            if self.num_tick is 0:
                self.record_timer.setSingleShot(True)
                self.record_timer.start(self.record_time*1000) # Set the timer in [ms]
            
            # put data into single iterable (numpy array)
            # put in timestamp
            row_to_write = np.array([time])
            # add A,B,C,D and raw coincidence counts
            row_to_write = np.append(row_to_write, num_data)
            # add stat correction to conincidence counts
            row_to_write = np.append(row_to_write, np.array([stat_AB,stat_AC,stat_AD,stat_BC,
                    stat_BD, stat_CD, stat_ABC, stat_BCD, stat_ABD, stat_ACD, stat_ABCD]))
            # add corrected coincidence counts
            row_to_write = np.append(row_to_write, np.array([num_data[4]-stat_AB,num_data[5]-stat_AC,   
                    num_data[6]-stat_AD,num_data[7]-stat_BC, num_data[8]-stat_BD, num_data[9]-stat_CD, 
                    num_data[10]-stat_ABC, num_data[11]-stat_BCD, num_data[12]-stat_ABD, num_data[13]-stat_ACD,
                    num_data[14]-stat_ABCD]))
            self.csv_writer.writerow(row_to_write)
            self.record_time_remained.setText('Time remaining: {:.1f} (s)'.format(self.record_time-self.update_period*self.num_tick))
            self.num_tick += 1

    def on_stop(self):
        """ stop and clear the serial thread """

        # if data recording in progress, stop record
        if self.record_active:
            self.on_record()
            
        # stop and disconnect the timer that triggers data retrieval
        self.disconnect(self.timer, QtCore.SIGNAL('timeout()'), self.on_update_timer)
        self.timer.stop()
        if self.serial_monitor != None:
            self.serial_monitor.pause = True
        
        
    def on_quit(self):
        """ stop and clear the serial thread if not yet done,
            and close the GUI
        """

        if self.serial_monitor is not None:
            self.serial_monitor.alive.clear()
            # join will wait until the thread terminates,
            # or the specified timeout = 0.01
            self.serial_monitor.join(0.001)
            self.serial_monitor = None
        
        self.close()

    def on_update_spinbox_change(self):
        """ when the update_spinbox is changed, change the update period timer """
        self.update_period = self.update_spin.value()
        
        if self.timer.isActive():
            self.timer.setInterval(self.update_period*1000.0)

    def on_record(self):
        """ record data for the amount of time specified in the input box
            OR if recording has already started, stop and export the data """

        # Check if recording is currently active, if it is then stop
        if self.record_active:
            self.record_active = False
            # Stop the timer and force it to send a timeout signal
            self.record_timer.stop()
            # Creates a new 1 ms timer to timeout immediately
            self.record_timer.start(1) 
            
        else: # Recording is not currently active
            # Set spinboxes to read-only
            self.record_spin.setReadOnly(True)
            self.update_spin.setReadOnly(True)
            self.coincidence_spin.setReadOnly(True)
            
            # Get amount of recording time from spinbox
            self.record_time = self.record_spin.value()

            # Set active flag and change button label
            self.record_active = True
            self.record_button.setText('Stop Recording')
            self.record_time_remained = QtGui.QLabel('Time remaining: {:.1f} (s)'.format(self.record_time))
            self.settings_grid.addWidget(self.record_time_remained, 5,1, QtCore.Qt.AlignCenter)
            
            # Connect timer trigger to on_timer method
            self.connect(self.record_timer, QtCore.SIGNAL('timeout()'), self.on_record_timer)
            
            # Number of data points saved
            self.num_tick = 0
            
            # Create csv file to save data in 
            self.path = './'
            self.output_file = open(self.path+datetime.datetime.now().strftime("%Y%m%d_%H%M%S")+'.csv', 'w', newline='')
            fieldnames = ['time','A','B','C','D','raw AB','raw AC','raw AD','raw BC','raw BD',
                    'raw CD','raw ABC','raw BCD','raw ACD','raw ABD','raw ABCD',
                    'stat correction AB','stat correction AC', 'stat correction AD','stat correction BC',
                    'stat correction BD','stat correction CD','stat correction ABC','stat correction BCD',
                    'stat correction ACD','stat correction ABD','stat correction ABCD',
                    'corrected AB','corrected AC', 'corrected AD','corrected BC',
                    'corrected BD','corrected CD','corrected ABC','corrected BCD',
                    'corrected ACD','corrected ABD','corrected ABCD']
            self.csv_writer = csv.writer(self.output_file)
            self.csv_writer.writerow(fieldnames)

            # check if data collection is on:
            if self.serial_monitor==None or self.serial_monitor.pause:
                self.on_start()
            
    def on_record_timer(self):
        """ Executed when the timer keeping track of data recording finishes """

        # Deactivate the recording flag
        self.record_active = False
        # Flush and close the csv file
        self.output_file.flush()
        self.output_file.close()
        # Change the button text to indicate that recording has finished
        self.record_button.setChecked(False)
        self.record_button.setText('Start Recording')
        
        # Set label back
        self.record_time_remained.setText('')
        
        # Unlock spinboxes
        self.record_spin.setReadOnly(False)
        self.update_spin.setReadOnly(False)
        self.coincidence_spin.setReadOnly(False)
    
    def get_item_from_queue(self, Q, timeout=0.001):
        """ Attempts to retrieve an item from the queue Q. If Q is
            empty, None is returned.
    
            Blocks for 'timeout' seconds in case the queue is empty.
        """
        try: 
            item = Q.get(True, timeout)
        except queue.Empty: 
            return None
            
        return item
        
def main():
    parser = argparse.ArgumentParser(description='Run QIE GUI code.')
    parser.add_argument('--portname')
    app = QtGui.QApplication(sys.argv)
    args = parser.parse_args()
    portname = args.portname
    gui = QIE_Gui(portname)
    gui.show()
    app.exec_()
    
if __name__ == '__main__':
    main()

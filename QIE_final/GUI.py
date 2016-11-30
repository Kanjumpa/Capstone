#!/usr/bin/env python3

from PyQt4 import QtGui, QtCore

import sys
import serial_data
import queue
import numpy as np


from utils import get_item_from_queue
from Skeleton import GuiSkeleton


class QIE_Gui(GuiSkeleton):
    """ 
        Class that manages backend functions of the GUI parts.
        Comments are made extensive for first-time PyQt4 and Thread module users.
    """
   
    def __init__(self):
        
        # Initialize the GUI: create all the GUI parts and layouts
        super(QIE_Gui, self).__init__()
        
        self.data_q = None
        self.error_q = None
        self.timer = QtCore.QTimer()
        self.record_timer = QtCore.QTimer()
        self.serial_monitor = None
        self.record_active = False
        self.portname = '/dev/tty.wchusbserial1410'
        
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
        
        # If there is already a serial thread running (start has been hit,
        # and not stopped yet) or portname not specified, return.
        if self.serial_monitor is not None or self.portname == '':
            return
        
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
        serial_error = get_item_from_queue(self.error_q)
        if serial_error is not None:
            QtGui.QMessageBox.critical(self, 'SerialThread error', serial_error)
            self.serial_monitor = None
       
        # Set active flag
        self.serial_active = True
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
        qdata = get_item_from_queue(self.data_q)
        time = qdata[0]
        num_data = qdata[1]
        for i in range(update_num-1):
            qdata = get_item_from_queue(self.data_q)
            num_data += data[1]
        
        if qdata is not None:
            # Calculate statistical corrections.
            # Retrieve coincidence timewindow
            time_window = self.coincidence_spin.value()
            
            raw_A = num_data[0]
            raw_B = num_data[1]
            raw_C = num_data[2]
            raw_D = num_data[3]
        
            stat_AB = 2*raw_A*raw_B*time_window*10**(-9)/update_period
            stat_AC = 2*raw_A*raw_C*time_window*10**(-9)/update_period
            stat_AD = 2*raw_A*raw_D*time_window*10**(-9)/update_period
            stat_BC = 2*raw_B*raw_C*time_window*10**(-9)/update_period
            stat_BD = 2*raw_B*raw_D*time_window*10**(-9)/update_period
            stat_CD = 2*raw_D*raw_D*time_window*10**(-9)/update_period
            stat_ABC = stat_AB*raw_C
            stat_BCD = stat_BC*raw_D
            stat_ABD = stat_AB*raw_D
            stat_ACD = stat_AC*raw_D
            stat_ABCD = stat_ABC*raw_D
            
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
            
            self.AB_stat_display.setText("{:.0f}".format(stat_AB))
            self.AC_stat_display.setText("{:.0f}".format(stat_AC))
            self.AD_stat_display.setText("{:.0f}".format(stat_AD))
            self.BC_stat_display.setText("{:.0f}".format(stat_BC))
            self.BD_stat_display.setText("{:.0f}".format(stat_BD))
            self.CD_stat_display.setText("{:.0f}".format(stat_CD))
            self.ABC_stat_display.setText("{:.0f}".format(stat_ABC))
            self.BCD_stat_display.setText("{:.0f}".format(stat_BCD))
            self.ABD_stat_display.setText("{:.0f}".format(stat_ABD))
            self.ACD_stat_display.setText("{:.0f}".format(stat_ACD))
            self.ABCD_stat_display.setText("{:.0f}".format(stat_ABCD))
            
            self.AB_stat_display.setText("{:.0f}".format(stat_AB))
            self.AC_stat_display.setText("{:.0f}".format(stat_AC))
            self.AD_stat_display.setText("{:.0f}".format(stat_AD))
            self.BC_stat_display.setText("{:.0f}".format(stat_BC))
            self.BD_stat_display.setText("{:.0f}".format(stat_BD))
            self.CD_stat_display.setText("{:.0f}".format(stat_CD))
            self.ABC_stat_display.setText("{:.0f}".format(stat_ABC))
            self.BCD_stat_display.setText("{:.0f}".format(stat_BCD))
            self.ABD_stat_display.setText("{:.0f}".format(stat_ABD))
            self.ACD_stat_display.setText("{:.0f}".format(stat_ACD))
            self.ABCD_stat_display.setText("{:.0f}".format(stat_ABCD))
            
            self.AB_corrected_display.setText("{:.0f}".format(num_data[4]-stat_AB))
            self.AC_corrected_display.setText("{:.0f}".format(num_data[5]-stat_AC))
            self.AD_corrected_display.setText("{:.0f}".format(num_data[6]-stat_AD))
            self.BC_corrected_display.setText("{:.0f}".format(num_data[7]-stat_BC))
            self.BD_corrected_display.setText("{:.0f}".format(num_data[8]-stat_BD))
            self.CD_corrected_display.setText("{:.0f}".format(num_data[9]-stat_CD))
            self.ABC_corrected_display.setText("{:.0f}".format(num_data[10]-stat_ABC))
            self.BCD_corrected_display.setText("{:.0f}".format(num_data[11]-stat_BCD))
            self.ABD_corrected_display.setText("{:.0f}".format(num_data[12]-stat_ABD))
            self.ACD_corrected_display.setText("{:.0f}".format(num_data[13]-stat_ACD))
            self.ABCD_corrected_display.setText("{:.0f}".format(num_data[14]-stat_ABCD))

        # Check if data recording is active and store the data from this tick if so
        if self.record_active:

            self.saved_data.put(time, num_data)
            

    def on_stop(self):
        """ stop and clear the serial thread """

        if self.serial_monitor is not None:
            self.serial_monitor.alive.clear()
            # join will wait until the thread terminates,
            # or the specified timeout = 0.01
            self.serial_monitor.join(0.01)
            self.serial_monitor = None
        # stop the timer that triggers data retrieval
        self.timer.stop()

    def on_quit(self):
        """ stop and clear the serial thread if not yet done,
            and close the GUI
        """

        if self.serial_monitor is not None:
            self.on_stop()
        
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

            # Stop the timer and force it to send a timeout signal
            self.record_timer.stop()
            self.record_timer.start(1) # Creates a new 1 ms timer to timeout immediately
            
        else: # Recording is not currently active

            # Get amount of recording time from spinbox
            self.record_time = self.record_spin.value()

            # Set active flag and change button label
            self.record_active = True
            self.record_button.setText('Stop Recording')

            # Create structure to save data in
            #num_data_points = self.record_time / (self.update_period*1000)        
            #self.saved_data = np.zeros(num_ticks)

            # Connect timer trigger to on_timer method
            self.connect(self.record_timer, QtCore.SIGNAL('timeout()'), self.on_record_timer)
            # Start the timer
            self.record_timer.setSingleShot(True)
            self.record_timer.start(self.record_time*1000) # Set the timer in [ms]

    def on_record_timer(self):
        """ Executed when the timer keeping track of data recording finishes """

        # Deactivate the recording flag
        self.record_active = False
        # Change the button text to indicate that recording has finished
        self.record_button.setText('Start Recording')
        
        
def main():
    app = QtGui.QApplication(sys.argv)
    gui = QIE_Gui()
    gui.show()
    app.exec_()
    
if __name__ == '__main__':
    main()

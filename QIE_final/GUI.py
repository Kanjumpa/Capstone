#!/usr/bin/env python3

import sys
from PyQt4 import QtGui, QtCore

import serial_data
import queue
import numpy as np
from utils import get_item_from_queue


class QIE_Gui(QtGui.QWidget):
    def __init__(self):
        super(QIE_Gui, self).__init__()
        
        self.serial_active = False
        self.serial_monitor = None
        self.data_q = None
        self.error_q = None
        self.portname = '/dev/tty.wchusbserial1410'
        
        self.timer = QtCore.QTimer()
        self.create_main()
    
    def create_main(self):
        # retrive subgrid layouts
        self.A, self.B, self.C, self.D, self.display_grid = self.create_data_display()
        self.quit_btn, self.start_btn, self.stop_btn, self.update_spin, self.button_grid = self.create_buttons()
        
        # create main window layout
        self.total_grid = QtGui.QGridLayout()
        self.total_grid.addLayout(self.button_grid, 1,0)
        self.total_grid.addLayout(self.display_grid, 1,1)
        self.setLayout(self.total_grid)
        self.setGeometry(300,300,600,20)
        self.setWindowTitle('example')
        self.center()
        
        # connect buttons to functions
        #self.quit_btn.clicked.connect(self.close)
        QtCore.QObject.connect(self.quit_btn, QtCore.SIGNAL("clicked()"), self.close)
        QtCore.QObject.connect(self.start_btn, QtCore.SIGNAL("clicked()"), self.on_start)
        QtCore.QObject.connect(self.stop_btn, QtCore.SIGNAL("clicked()"), self.on_stop)
        QtCore.QObject.connect(self.update_spin, QtCore.SIGNAL("valueChanged(double)"), self.on_spinbox_change)
        
    def create_data_display(self):
        
        A_label = QtGui.QLabel('A')
        B_label = QtGui.QLabel('B')
        C_label = QtGui.QLabel('C')
        D_label = QtGui.QLabel('D')
        
        A_display = QtGui.QLineEdit()
        A_display.setReadOnly(True)
        
        B_display = QtGui.QLineEdit()
        B_display.setReadOnly(True)
        
        C_display = QtGui.QLineEdit()
        C_display.setReadOnly(True)
        
        D_display = QtGui.QLineEdit()
        D_display.setReadOnly(True)
        
        upper_display_grid = QtGui.QGridLayout()
        upper_display_grid.setSpacing(10)
        
        upper_display_grid.addWidget(A_display, 1, 0)
        upper_display_grid.addWidget(A_label, 2, 0, QtCore.Qt.AlignCenter)
        
        upper_display_grid.addWidget(B_display, 1, 1)
        upper_display_grid.addWidget(B_label, 2, 1, QtCore.Qt.AlignCenter)
        
        upper_display_grid.addWidget(C_display, 1, 2)
        upper_display_grid.addWidget(C_label, 2, 2, QtCore.Qt.AlignCenter)
        
        upper_display_grid.addWidget(D_display, 1, 3)
        upper_display_grid.addWidget(D_label, 2, 3, QtCore.Qt.AlignCenter)
        
        return A_display, B_display, C_display, D_display, upper_display_grid
        
        
    def create_buttons(self):
        quit_button = QtGui.QPushButton('Quit', self)
        quit_button.resize(quit_button.sizeHint())
        
        start_button = QtGui.QPushButton('Start', self)
        start_button.resize(start_button.sizeHint())
        
        stop_button = QtGui.QPushButton('Stop', self)
        stop_button.resize(stop_button.sizeHint())
        
        update_spin = QtGui.QDoubleSpinBox(self)
        update_spin.setSingleStep(0.1)
        update_spin.setRange(0.1,5.0)
        update_spin.setDecimals(1)
        
        button_grid = QtGui.QGridLayout()
        button_grid.setSpacing(10)
        
        button_grid.addWidget(quit_button, 1,0)
        button_grid.addWidget(start_button, 2,0)
        button_grid.addWidget(stop_button, 3,0)
        button_grid.addWidget(update_spin, 4,0)
        
        return quit_button, start_button, stop_button, update_spin, button_grid
      
    def on_start(self):
        """ Start the serial thread and update timer """
        
        # test to see that function triggered
        if self.serial_monitor is not None or self.portname == '':
            return
       
        print("serial port open")

        self.data_q = queue.Queue()
        self.error_q = queue.Queue()
        
        self.serial_monitor = serial_data.SerialThread(
                self.data_q,
                self.error_q,
                self.portname)
                
        self.serial_monitor.start()
        
        serial_error = get_item_from_queue(self.error_q)
        if serial_error is not None:
            QtGui.QMessageBox.critical(self, 'SerialThread error', serial_error)
            self.serial_monitor = None
       
        print("thread started without error") 
        self.serial_active = True
        self.update_period = self.update_spin.value()
        self.timer = QtCore.QTimer()
        self.connect(self.timer, QtCore.SIGNAL('timeout()'), self.on_timer)
        self.timer.start(self.update_period*1000.0)

    
    def on_timer(self):
        """ Executed periodically when the serial update timer is fired 
        """
        # print("GUI:on_timer::update_period is ", self.update_period)
        update_num = int(round(self.update_period/0.1))
        # print("GUI:on_timer::update_num is ", update_num)
        qdata = get_item_from_queue(self.data_q)
        for i in range(update_num-1):
            qdata += get_item_from_queue(self.data_q)
            # print("qdata %s: "%i, qdata)
        if qdata is not None:
            A_string = "{:.0f}".format(qdata[0]) 
            B_string = "{:.0f}".format(qdata[1]) 
            C_string = "{:.0f}".format(qdata[2]) 
            D_string = "{:.0f}".format(qdata[3]) 
            self.A.setText(A_string)
            self.B.setText(B_string)
            self.C.setText(C_string)
            self.D.setText(D_string)

    def on_stop(self):
        """ stop and clear the serial thread """

        if self.serial_monitor is not None:
            self.serial_monitor.alive.clear()
            self.serial_monitor.join(0.01)
            self.serial_monitor = None
        self.timer.stop()

    def on_spinbox_change(self):
        """ when the spinbox is changed, change the update period timer """
        self.update_period = self.update_spin.value()
       
        if self.timer.isActive():
            self.timer.setInterval(self.update_period*1000.0)
        
    def center(self):
        qr = self.frameGeometry()
        cp = QtGui.QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())
        
def main():
    app = QtGui.QApplication(sys.argv)
    gui = QIE_Gui()
    gui.show()
    app.exec_()
    
if __name__ == '__main__':
    main()

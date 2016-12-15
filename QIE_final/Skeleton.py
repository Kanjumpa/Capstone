#!/usr/bin/env python3

from PyQt4 import QtGui, QtCore


class GuiSkeleton(QtGui.QWidget):
    """ Class that creates all the GUI parts (buttons, displays, labels...)
        and arrange the layouts.
        Comments are made extensive for first-time PyQt4 users.
    """
   
    def __init__(self):
        super(GuiSkeleton, self).__init__()
        
        self.serial_active = False
        self.serial_monitor = None
        self.data_q = None
        self.error_q = None
        # Name of serial port; right now only comparitble with Mac
        self.portname = '/dev/tty.wchusbserial1410'
        
        self.timer = QtCore.QTimer()
        self.create_main_window()
    
    def create_main_window(self):
        """ create the main GUI window, and connect the buttons/spinboxes to 
            methods that will be run when the buttons/spinboxes are triggered
            by user action
        """
        
        # main window is made from three QGroupBoxes: Settings, 
        # Single Photon Counts, and Coincidence Counts.
        # A QGroupBox makes multiple QWidgets (buttons, displays...)
        # functionally and visually related for easier management.
        # Create the QGroupBoxes using custon method:
        self.create_single_photon_box()
        self.create_settings_box()
        self.create_coincidence_photon_box()
        
        # Put the QGroupBoxes into QGridLayout for easy layouting.
        # QGridLayout puts objects into grids, so don't need to layout
        # by tedious coordinates.
        # Create the grid for the main window
        self.total_grid = QtGui.QGridLayout()
        # Put the Settings group
        self.total_grid.addWidget(self.settings_box, 0, 0, 3, 1)
        # Put the Single Photon Count group in first row, second column [0,1],
        # spanning one cell [1,1]
        self.total_grid.addWidget(self.single_photon_box, 0, 1)
        # Put empty space for asthetic purposes
        #spacer1 = QtGui.QSpacerItem(300,1)
        #self.total_grid.addItem(spacer1, 0, 2)
        # Put the Coincidence Count group
        self.total_grid.addWidget(self.coincidence_photon_box, 2, 1, 1, 2)
        # Set the created layout
        self.setLayout(self.total_grid)
        # Set the size of the main window
        self.setGeometry(100,300,600,20)
        # Set the title of the main window
        self.setWindowTitle('Quantum Interference and Entanglement GUI')
        
        # Center the main window in the screen using custum method
        #self.center()
        
    def create_single_photon_box(self):
        """ create the QGroupBox containing displays and labels for
            single photon counts.
        """
        
        # Create QGroupBox
        self.single_photon_box = QtGui.QGroupBox()
        # Set title for the GroupBox
        self.single_photon_box.setTitle("Single Photon Counts")
        
        # Create a QGridLayout for easy layouting inside the GroupBox
        self.single_photon_grid = QtGui.QGridLayout()
        
        # Create Labels
        self.A_label = QtGui.QLabel('A')
        self.B_label = QtGui.QLabel('B')
        self.C_label = QtGui.QLabel('C')
        self.D_label = QtGui.QLabel('D')
        
        # Create text displays and set to read only
        self.A_display = QtGui.QLineEdit()
        self.A_display.setReadOnly(True)
        #self.A_display.setFixedWidth(80)
        
        self.B_display = QtGui.QLineEdit()
        self.B_display.setReadOnly(True)
        #self.B_display.setFixedWidth(80)
        
        self.C_display = QtGui.QLineEdit()
        self.C_display.setReadOnly(True)
        #self.C_display.setFixedWidth(80)
        
        self.D_display = QtGui.QLineEdit()
        self.D_display.setReadOnly(True)
        #self.D_display.setFixedWidth(80)
        
        # Arrange the labels and displays in the GridLayout
        self.single_photon_grid.addWidget(self.A_display, 1, 0)
        self.single_photon_grid.addWidget(self.A_label, 0, 0, QtCore.Qt.AlignCenter)
        
        self.single_photon_grid.addWidget(self.B_display, 1, 1)
        self.single_photon_grid.addWidget(self.B_label, 0, 1, QtCore.Qt.AlignCenter)
        
        self.single_photon_grid.addWidget(self.C_display, 1, 2)
        self.single_photon_grid.addWidget(self.C_label, 0, 2, QtCore.Qt.AlignCenter)
        
        self.single_photon_grid.addWidget(self.D_display, 1, 3)
        self.single_photon_grid.addWidget(self.D_label, 0, 3, QtCore.Qt.AlignCenter)

        # Apply the grid layout into the GroupBox
        self.single_photon_box.setLayout(self.single_photon_grid)
        
    def create_coincidence_photon_box(self):
        """ create the QGroupBox containing displays and labels for
            single photon counts.
        """
        
        # Create QGroupBox
        self.coincidence_photon_box = QtGui.QGroupBox()
        # Set title for the GroupBox
        self.coincidence_photon_box.setTitle("Coincidence Photon Counts")
        
        # Create a QGridLayout for easy layouting inside the GroupBox
        self.coincidence_photon_grid = QtGui.QGridLayout()
        
        # Create Labels
        self.AB_label = QtGui.QLabel('AB')
        self.AC_label = QtGui.QLabel('AC')
        self.AD_label = QtGui.QLabel('AD')
        self.BC_label = QtGui.QLabel('BC')
        self.BD_label = QtGui.QLabel('BD')
        self.CD_label = QtGui.QLabel('CD')
        self.ABC_label = QtGui.QLabel('ABC')
        self.BCD_label = QtGui.QLabel('BCD')
        self.ACD_label = QtGui.QLabel('ACD')
        self.ABD_label = QtGui.QLabel('ABD')
        self.ABCD_label = QtGui.QLabel('ABCD')
        
        self.raw_label = QtGui.QLabel('Raw Coincidence')
        self.stat_label = QtGui.QLabel('Statistical Correction')
        self.corrected_label = QtGui.QLabel('Corrected Coincidence')
        
        # Create text displays, set to read only, set width
        self.AB_raw_display = QtGui.QLineEdit()
        self.AB_raw_display.setReadOnly(True)
        self.AB_raw_display.setMinimumWidth(70)
        self.AB_stat_display = QtGui.QLineEdit()
        self.AB_stat_display.setReadOnly(True)
        self.AB_stat_display.setMinimumWidth(70)
        self.AB_corrected_display = QtGui.QLineEdit()
        self.AB_corrected_display.setReadOnly(True)
        self.AB_corrected_display.setMinimumWidth(70)

        
        self.AC_raw_display = QtGui.QLineEdit()
        self.AC_raw_display.setReadOnly(True)
        self.AC_raw_display.setMinimumWidth(70)
        self.AC_stat_display = QtGui.QLineEdit()
        self.AC_stat_display.setReadOnly(True)
        self.AC_stat_display.setMinimumWidth(70)
        self.AC_corrected_display = QtGui.QLineEdit()
        self.AC_corrected_display.setReadOnly(True)
        self.AC_corrected_display.setMinimumWidth(70)
        
        self.AD_raw_display = QtGui.QLineEdit()
        self.AD_raw_display.setReadOnly(True)
        self.AD_raw_display.setMinimumWidth(70)
        self.AD_stat_display = QtGui.QLineEdit()
        self.AD_stat_display.setReadOnly(True)
        self.AD_raw_display.setMinimumWidth(70)
        self.AD_corrected_display = QtGui.QLineEdit()
        self.AD_corrected_display.setReadOnly(True)
        self.AD_raw_display.setMinimumWidth(70)
        
        self.BC_raw_display = QtGui.QLineEdit()
        self.BC_raw_display.setReadOnly(True)
        self.BC_raw_display.setMinimumWidth(70)
        self.BC_stat_display = QtGui.QLineEdit()
        self.BC_stat_display.setReadOnly(True)
        self.BC_stat_display.setMinimumWidth(70);
        self.BC_corrected_display = QtGui.QLineEdit()
        self.BC_corrected_display.setReadOnly(True)
        self.BC_corrected_display.setMinimumWidth(70)
        
        self.BD_raw_display = QtGui.QLineEdit()
        self.BD_raw_display.setReadOnly(True)
        self.BD_raw_display.setMinimumWidth(70)
        self.BD_stat_display = QtGui.QLineEdit()
        self.BD_stat_display.setReadOnly(True)
        self.BD_stat_display.setMinimumWidth(70)
        self.BD_corrected_display = QtGui.QLineEdit()
        self.BD_corrected_display.setReadOnly(True)
        self.BD_corrected_display.setMinimumWidth(70)
        
        self.CD_raw_display = QtGui.QLineEdit()
        self.CD_raw_display.setReadOnly(True)
        self.CD_raw_display.setMinimumWidth(70)
        self.CD_stat_display = QtGui.QLineEdit()
        self.CD_stat_display.setReadOnly(True)
        self.CD_stat_display.setMinimumWidth(70)
        self.CD_corrected_display = QtGui.QLineEdit()
        self.CD_corrected_display.setReadOnly(True)
        self.CD_corrected_display.setMinimumWidth(70)
        
        self.ABC_raw_display = QtGui.QLineEdit()
        self.ABC_raw_display.setReadOnly(True)
        self.ABC_raw_display.setMinimumWidth(70)
        self.ABC_stat_display = QtGui.QLineEdit()
        self.ABC_stat_display.setReadOnly(True)
        self.ABC_stat_display.setMinimumWidth(70)
        self.ABC_corrected_display = QtGui.QLineEdit()
        self.ABC_corrected_display.setReadOnly(True)
        self.ABC_corrected_display.setMinimumWidth(70)
        
        self.BCD_raw_display = QtGui.QLineEdit()
        self.BCD_raw_display.setReadOnly(True)
        self.BCD_raw_display.setMinimumWidth(70)
        self.BCD_stat_display = QtGui.QLineEdit()
        self.BCD_stat_display.setReadOnly(True)
        self.BCD_stat_display.setMinimumWidth(70)
        self.BCD_corrected_display = QtGui.QLineEdit()
        self.BCD_corrected_display.setReadOnly(True)
        self.BCD_corrected_display.setMinimumWidth(70)
        
        self.ACD_raw_display = QtGui.QLineEdit()
        self.ACD_raw_display.setReadOnly(True)
        self.ACD_raw_display.setMinimumWidth(70)
        self.ACD_stat_display = QtGui.QLineEdit()
        self.ACD_stat_display.setReadOnly(True)
        self.ACD_stat_display.setMinimumWidth(70)
        self.ACD_corrected_display = QtGui.QLineEdit()
        self.ACD_corrected_display.setReadOnly(True)
        self.ACD_corrected_display.setMinimumWidth(70)
        
        self.ABD_raw_display = QtGui.QLineEdit()
        self.ABD_raw_display.setReadOnly(True)
        self.ABD_raw_display.setMinimumWidth(70)
        self.ABD_stat_display = QtGui.QLineEdit()
        self.ABD_stat_display.setReadOnly(True)
        self.ABD_stat_display.setMinimumWidth(70)
        self.ABD_corrected_display = QtGui.QLineEdit()
        self.ABD_corrected_display.setReadOnly(True)
        self.ABD_corrected_display.setMinimumWidth(70)
        
        self.ABCD_raw_display = QtGui.QLineEdit()
        self.ABCD_raw_display.setReadOnly(True)
        self.ABCD_raw_display.setMinimumWidth(70)
        self.ABCD_stat_display = QtGui.QLineEdit()
        self.ABCD_stat_display.setReadOnly(True)
        self.ABCD_stat_display.setMinimumWidth(70)
        self.ABCD_corrected_display = QtGui.QLineEdit()
        self.ABCD_corrected_display.setReadOnly(True)
        self.ABCD_corrected_display.setMinimumWidth(70)
        
        # Arrange the labels and displays in the GridLayout
        self.coincidence_photon_grid.addWidget(self.AB_label, 0, 1, QtCore.Qt.AlignCenter)
        self.coincidence_photon_grid.addWidget(self.AC_label, 0, 2, QtCore.Qt.AlignCenter)
        self.coincidence_photon_grid.addWidget(self.AD_label, 0, 3, QtCore.Qt.AlignCenter)
        self.coincidence_photon_grid.addWidget(self.BC_label, 0, 4, QtCore.Qt.AlignCenter)
        self.coincidence_photon_grid.addWidget(self.BD_label, 0, 5, QtCore.Qt.AlignCenter)
        self.coincidence_photon_grid.addWidget(self.CD_label, 0, 6, QtCore.Qt.AlignCenter)
        self.coincidence_photon_grid.addWidget(self.ABC_label, 4, 1, QtCore.Qt.AlignCenter)
        self.coincidence_photon_grid.addWidget(self.BCD_label, 4, 2, QtCore.Qt.AlignCenter)
        self.coincidence_photon_grid.addWidget(self.ACD_label, 4, 3, QtCore.Qt.AlignCenter)
        self.coincidence_photon_grid.addWidget(self.ABD_label, 4, 4, QtCore.Qt.AlignCenter)
        self.coincidence_photon_grid.addWidget(self.ABCD_label, 4, 5, QtCore.Qt.AlignCenter)
        
        self.coincidence_photon_grid.addWidget(self.corrected_label, 1,0)        
        self.coincidence_photon_grid.addWidget(self.AB_corrected_display, 1, 1)
        self.coincidence_photon_grid.addWidget(self.AC_corrected_display, 1, 2)
        self.coincidence_photon_grid.addWidget(self.AD_corrected_display, 1, 3)
        self.coincidence_photon_grid.addWidget(self.BC_corrected_display, 1, 4)
        self.coincidence_photon_grid.addWidget(self.BD_corrected_display, 1, 5)
        self.coincidence_photon_grid.addWidget(self.CD_corrected_display, 1, 6)
        self.coincidence_photon_grid.addWidget(self.ABC_corrected_display, 5, 1)
        self.coincidence_photon_grid.addWidget(self.BCD_corrected_display, 5, 2)
        self.coincidence_photon_grid.addWidget(self.ACD_corrected_display, 5, 3)
        self.coincidence_photon_grid.addWidget(self.ABD_corrected_display, 5, 4)
        self.coincidence_photon_grid.addWidget(self.ABCD_corrected_display, 5, 5)
        
        self.coincidence_photon_grid.addWidget(self.stat_label, 2,0)
        self.coincidence_photon_grid.addWidget(self.AB_stat_display, 2, 1)
        self.coincidence_photon_grid.addWidget(self.AC_stat_display, 2, 2)
        self.coincidence_photon_grid.addWidget(self.AD_stat_display, 2, 3)
        self.coincidence_photon_grid.addWidget(self.BC_stat_display, 2, 4)
        self.coincidence_photon_grid.addWidget(self.BD_stat_display, 2, 5)
        self.coincidence_photon_grid.addWidget(self.CD_stat_display, 2, 6)
        self.coincidence_photon_grid.addWidget(self.ABC_stat_display, 6, 1)
        self.coincidence_photon_grid.addWidget(self.BCD_stat_display, 6, 2)
        self.coincidence_photon_grid.addWidget(self.ACD_stat_display, 6, 3)
        self.coincidence_photon_grid.addWidget(self.ABD_stat_display, 6, 4)
        self.coincidence_photon_grid.addWidget(self.ABCD_stat_display, 6, 5)
        
        self.coincidence_photon_grid.addWidget(self.raw_label, 3,0)
        self.coincidence_photon_grid.addWidget(self.AB_raw_display, 3, 1)
        self.coincidence_photon_grid.addWidget(self.AC_raw_display, 3, 2)
        self.coincidence_photon_grid.addWidget(self.AD_raw_display, 3, 3)
        self.coincidence_photon_grid.addWidget(self.BC_raw_display, 3, 4)
        self.coincidence_photon_grid.addWidget(self.BD_raw_display, 3, 5)
        self.coincidence_photon_grid.addWidget(self.CD_raw_display, 3, 6)
        self.coincidence_photon_grid.addWidget(self.ABC_raw_display, 7, 1)
        self.coincidence_photon_grid.addWidget(self.BCD_raw_display, 7, 2)
        self.coincidence_photon_grid.addWidget(self.ACD_raw_display, 7, 3)
        self.coincidence_photon_grid.addWidget(self.ABD_raw_display, 7, 4)
        self.coincidence_photon_grid.addWidget(self.ABCD_raw_display, 7, 5)
        
        # Apply the grid layout into the GroupBox
        self.coincidence_photon_box.setLayout(self.coincidence_photon_grid)
        
    def create_settings_box(self):
        """ create the QGroupBox containing all buttons and spinboxes
        """
        # Create QGroupBox
        self.settings_box = QtGui.QGroupBox()
        # Set title for the GroupBox
        self.settings_box.setTitle("Settings")
        
        # Create buttons for Quit, Start, Stop and Record data
        self.quit_button = QtGui.QPushButton('Quit', self)
        self.quit_button.setFixedWidth(160)
        self.quit_button.setFixedHeight(60)
        
        self.start_button = QtGui.QPushButton('Start', self)
        self.start_button.setFixedWidth(100)
        
        self.stop_button = QtGui.QPushButton('Stop', self)
        self.stop_button.setFixedWidth(100)
        
        self.record_button = QtGui.QPushButton('Start Recording', self)
        self.record_button.setCheckable(True)
        self.record_button.setFixedWidth(140)
        
        # Create spinboxes for update period, coincidence window and data recording time
        self.update_spin = QtGui.QDoubleSpinBox(self)
        self.update_spin.setFixedWidth(100)
        self.update_spin.setSingleStep(0.1)
        self.update_spin.setRange(0.1,10.0)
        self.update_spin.setValue(1.0)
        self.update_spin.setDecimals(1)
        self.update_spin_label = QtGui.QLabel('Update Period (s)')
        
        self.coincidence_spin = QtGui.QDoubleSpinBox(self)
        self.coincidence_spin.setFixedWidth(100)
        self.coincidence_spin.setSingleStep(0.5)
        self.coincidence_spin.setMinimum(1.0)
        self.coincidence_spin.setDecimals(1)
        self.coincidence_spin_label = QtGui.QLabel('Conincidence Window (ns)')
    
        self.record_spin = QtGui.QSpinBox(self)
        self.record_spin.setFixedWidth(100)
        self.record_spin_label = QtGui.QLabel('Record data for (s):')
        
        # Create a QGridLayout for easy layouting inside the GroupBox
        self.settings_grid = QtGui.QGridLayout()
        
        # Arrange the buttons and spinboxes into gridlayout
        # Empty space for asthetic purposes
        spacer1 = QtGui.QSpacerItem(100,10)
        spacer2 = QtGui.QSpacerItem(100,30)
        self.settings_grid.addWidget(self.start_button, 0,0, QtCore.Qt.AlignCenter)
        self.settings_grid.addWidget(self.stop_button, 0,1, QtCore.Qt.AlignCenter)
        self.settings_grid.addWidget(self.update_spin_label, 2,0, QtCore.Qt.AlignCenter)
        self.settings_grid.addWidget(self.update_spin, 3,0, QtCore.Qt.AlignCenter)
        self.settings_grid.addWidget(self.coincidence_spin_label, 2,1, QtCore.Qt.AlignCenter)
        self.settings_grid.addWidget(self.coincidence_spin, 3,1, QtCore.Qt.AlignCenter)
        self.settings_grid.addItem(spacer2, 4, 0)
        self.settings_grid.addWidget(self.record_spin_label, 5,0, QtCore.Qt.AlignCenter)
        self.settings_grid.addWidget(self.record_spin, 6,0, QtCore.Qt.AlignCenter)
        self.settings_grid.addWidget(self.record_button, 6,1, QtCore.Qt.AlignCenter)
        self.settings_grid.addItem(spacer2, 7, 0)
        self.settings_grid.addWidget(self.quit_button, 8,0, QtCore.Qt.AlignCenter)
        
        # Apply the grid layout to the groupbox
        self.settings_box.setLayout(self.settings_grid)
        
    def center(self):
        qr = self.frameGeometry()
        cp = QtGui.QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())
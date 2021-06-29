"""
Module: SceneViewerGUI.py
@author: Carlos Vinhais / Carlos Silva
cvinhais@gmail.com / 1160628@isep.ipp.pt
"""

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *

import SceneViewer
import os

""" A class for Scene Viewer GUI """

class Ui_MainWindow( object ):
    
    def setupUi(self, MainWindow):
        
        QApplication.setStyle('Fusion')
         
        # Main Window
        # -------------------------------------
        MainWindow.setObjectName("MainWindow")
        MainWindow.setWindowTitle("3D Indoor Mapping App")
        MainWindow.setWindowIcon( QtGui.QIcon('Projeto_GUI/isep.png') )
        self.centralWidget = QtWidgets.QWidget( MainWindow )
        # MainWindow.setCentralWidget( self.centralWidget )
        
        # Widgets
        # -------------------------------------
        self.CommunicationGroup("Communication")
        self.ImuGroup("IMU")
        self.MotorsGroup("Motors")
        self.ScanGroup("Scan")
        self.LogosGroup("Support:")
        
        self.qvtk1 = SceneViewer.SceneViewer()
        # self.qvtk2 = SceneViewer.SceneViewer()

        # Layouts
        # -------------------------------------
        layout1 = QVBoxLayout()
        layout1.setContentsMargins(0,0,0,0)
        layout1.addWidget( self.CommunicationGroup )
        layout1.addWidget( self.ImuGroup )
        layout1.addWidget( self.MotorsGroup )
        layout1.addWidget( self.ScanGroup )
        layout1.setAlignment( QtCore.Qt.AlignTop )       

        layout2 = QVBoxLayout()
        layout2.setContentsMargins(0,0,0,0)
        layout2.addWidget( self.qvtk1.iren )
        layout2.addWidget( self.LogosGroup )
        # layout2.addWidget( self.qvtk2.iren )
        
        layout = QHBoxLayout()
        layout.addLayout( layout1 )
        layout.addLayout( layout2 )

        # Frame
        # ------------------------------------- 
        self.frame = QFrame(self.centralWidget)
        self.frame.setFrameShape( QFrame.StyledPanel )
        self.frame.setLayout( layout )

        MainWindow.setCentralWidget( self.frame )

        # Menu Bar
        # -------------------------------------
        self.FileMenu = QMenu("&File")
        self.HelpMenu = QMenu("&Help")
        
        self.menuBar = MainWindow.menuBar()
        self.menuBar.addMenu( self.FileMenu )
        self.menuBar.addMenu( self.HelpMenu )
        
        self.FileNewAction      = self.FileMenu.addAction('New...')
        self.FileOpenAction     = self.FileMenu.addAction('Open...')
        self.FileSaveAction     = self.FileMenu.addAction('Save Point Cloud...')
        self.StatsSaveAction    = self.FileMenu.addAction('Save Statistics...')
        self.FileExportAction   = self.FileMenu.addAction('Export Screenshot...')
        self.AllSaveAction      = self.FileMenu.addAction('Save All...')
        self.FileQuitAction     = self.FileMenu.addAction('Quit')

        self.FileNewAction.setShortcut('Ctrl+N')
        self.FileOpenAction.setShortcut('Ctrl+O')
        self.FileSaveAction.setShortcut('Ctrl+S')
        self.FileExportAction.setShortcut('Ctrl+X')
        self.FileQuitAction.setShortcut('Ctrl+Q')
        
        self.HelpAboutAction = self.HelpMenu.addAction('About')
        self.HelpAboutAction.setShortcut('Ctrl+A')
        
        # Tool Bar
        # -------------------------------------
        icons = [
            'SP_DialogOpenButton',
            'SP_DialogApplyButton',
            'SP_DialogCancelButton',
            'SP_DialogResetButton',
            'SP_DialogDiscardButton',            
            'SP_DialogSaveButton',
            'SP_DialogCloseButton',
            'SP_DialogHelpButton',            
            'SP_CustomBase',
            'SP_ArrowBack',
            'SP_ArrowDown']
        # self.toolbar = MainWindow.addToolBar( '' )
        # for i in icons:        
        #     img = MainWindow.style().standardIcon(getattr(QStyle, i))
        #     action = QAction( img, i, MainWindow)
        #     action.setEnabled( 1 )
        #     self.toolbar.addAction( action ) 

        
        # self.action.triggered.connect( ... )
        
        # Status Bar
        # -------------------------------------
        self.statusBar = MainWindow.statusBar()
        self.statusBar.showMessage('Ready to connect')

    def SetMessageStatus(self, message ):
        self.statusBar.showMessage( message )

    # ===============================================

    def CommunicationGroup(self, title):
        # Widgets
        Label_USBPort = QLabel("USB Port:")
        self.lineEdit_USBPort = QLineEdit("/dev/ttyUSB0") # default value
        #self.lineEdit_USBPort = QLineEdit("COM3") # default value
        self.lineEdit_USBPort.setAlignment(QtCore.Qt.AlignCenter)

        Label_SSID = QLabel("SSID:")
        self.lineEdit_SSID = QLineEdit("Vodafone-48742C") # default value
        #self.lineEdit_SSID = QLineEdit("MikoAP") # default value
        self.lineEdit_SSID.setAlignment(QtCore.Qt.AlignCenter)

        Label_PWD = QLabel("Password:")
        self.lineEdit_PWD = QLineEdit() # default value

        self.lineEdit_PWD.setEchoMode(QLineEdit.Password)
        #self.lineEdit_PWD.setText("mikotrico")
        self.lineEdit_PWD.setText("nAs96k9mY2")
        self.lineEdit_PWD.setAlignment(QtCore.Qt.AlignCenter)

        Label_HOST = QLabel("Host IP:")
        self.lineEdit_HOST = QLineEdit("192.168.1.64") # default value
        #self.lineEdit_HOST = QLineEdit("192.168.1.91") # default value
        self.lineEdit_HOST.setAlignment(QtCore.Qt.AlignCenter)

        Label_PORT = QLabel("Port:")
        self.lineEdit_PORT = QLineEdit("5000") # default value
        self.lineEdit_PORT.setAlignment(QtCore.Qt.AlignCenter)
        
        Label_STATUS1 = QLabel("Status:")
        self.Label_STATUS2 = QLabel("Disconnected")
        self.Label_STATUS2flag = False
        self.Label_STATUS2.setAlignment(QtCore.Qt.AlignCenter)
        self.Label_STATUS2.setStyleSheet('color: red')

        Label_ScannerIP1 = QLabel("Scanner IP:")
        self.Label_ScannerIP2 = QLabel("xxx.xxx.xxx.xxx")
        self.Label_ScannerIP2.setAlignment(QtCore.Qt.AlignCenter)

        # Widgets: Buttons: UI Actions
        self.Button_Connect_COM = QPushButton( "Connect" )
        icon1 = 'SP_DialogApplyButton'
        img1 = self.centralWidget.style().standardIcon(getattr(QStyle, icon1))
        self.Button_Connect_COM.setIcon( img1 )
        self.Button_Connect_COM.setEnabled( 1 )

        self.Button_Disconnect_COM = QPushButton( "Disconnect" )
        icon2 = 'SP_DialogCancelButton'
        img2 = self.centralWidget.style().standardIcon(getattr(QStyle, icon2))
        self.Button_Disconnect_COM.setIcon( img2 )
        self.Button_Disconnect_COM.setEnabled( 0 )

        # Layout
        layout = QGridLayout()
        layout.addWidget( Label_USBPort, 0, 0)
        layout.addWidget( self.lineEdit_USBPort, 0, 1)
        layout.addWidget( Label_SSID, 1, 0)
        layout.addWidget( self.lineEdit_SSID, 1, 1)
        layout.addWidget( Label_PWD, 2, 0)
        layout.addWidget( self.lineEdit_PWD, 2, 1)
        layout.addWidget( Label_HOST, 3, 0)
        layout.addWidget( self.lineEdit_HOST, 3, 1)
        layout.addWidget( Label_PORT, 4, 0)
        layout.addWidget( self.lineEdit_PORT, 4, 1)
        layout.addWidget( Label_STATUS1, 5, 0)
        layout.addWidget( self.Label_STATUS2, 5, 1)
        layout.addWidget( Label_ScannerIP1, 6, 0)
        layout.addWidget( self.Label_ScannerIP2, 6, 1)
        layout.addWidget(self.Button_Connect_COM,  7, 0)
        layout.addWidget(self.Button_Disconnect_COM,  7, 1)
        # Group
        self.CommunicationGroup = QGroupBox( title )
        self.CommunicationGroup.setAlignment(QtCore.Qt.AlignCenter)
        self.CommunicationGroup.setStyleSheet("QGroupBox { font-weight: bold; } ")        
        self.CommunicationGroup.setLayout( layout )

        # -------------------------------------        
    
    def ImuGroup(self, title):

        IMUAccLabel1 = QLabel("Accelereometer:")
        self.IMUAccLabel2 = QLabel("No status")
        self.IMUAccLabel2.setStyleSheet('color: orange')
        self.IMUAccLabel2.setAlignment(QtCore.Qt.AlignCenter)
        self.IMUAccLabel3 = QLabel("No calibration")
        self.IMUAccLabel3.setStyleSheet('color: orange')
        self.IMUAccLabel3.setAlignment(QtCore.Qt.AlignCenter)


        IMUGyrLabel1 = QLabel("Gyroscope:")
        self.IMUGyrLabel2 = QLabel("No status")
        self.IMUGyrLabel2.setStyleSheet('color: orange')
        self.IMUGyrLabel2.setAlignment(QtCore.Qt.AlignCenter)
        self.IMUGyrLabel3 = QLabel("No calibration")
        self.IMUGyrLabel3.setStyleSheet('color: orange')
        self.IMUGyrLabel3.setAlignment(QtCore.Qt.AlignCenter)

        IMUMagLabel1 = QLabel("Magnetometer:")
        self.IMUMagLabel2 = QLabel("No status")
        self.IMUMagLabel2.setStyleSheet('color: orange')
        self.IMUMagLabel2.setAlignment(QtCore.Qt.AlignCenter)
        self.IMUMagLabel3 = QLabel("No calibration")
        self.IMUMagLabel3.setStyleSheet('color: orange')
        self.IMUMagLabel3.setAlignment(QtCore.Qt.AlignCenter)

        IMUMicLabel1 = QLabel("Microcontroller:")
        self.IMUMicLabel2 = QLabel("No status")
        self.IMUMicLabel2.setStyleSheet('color: orange')
        self.IMUMicLabel2.setAlignment(QtCore.Qt.AlignCenter)

        IMUSystemLabel1 = QLabel("System:")
        self.IMUSystemLabel2 = QLabel("No calibration")
        self.IMUSystemLabel2.setStyleSheet('color: orange')
        self.IMUSystemLabel2.setAlignment(QtCore.Qt.AlignCenter)

        self.button_CheckStatus      =  QPushButton( "Check Status" )
        self.button_StartCalibration =  QPushButton( "Calibrate" )
        self.button_StopCalibration  =  QPushButton( "Stop"  )
        
        icon1 = 'SP_DialogApplyButton'
        icon2 = 'SP_DialogCancelButton'
        icon3 = 'SP_MediaPlay'
        img1 = self.centralWidget.style().standardIcon(getattr(QStyle, icon1))
        img2 = self.centralWidget.style().standardIcon(getattr(QStyle, icon2))
        img3 = self.centralWidget.style().standardIcon(getattr(QStyle, icon3))

        self.button_CheckStatus.setIcon( img1 )
        self.button_StartCalibration.setIcon( img3 )
        self.button_StopCalibration.setIcon(  img2 )

        self.button_CheckStatus.setEnabled( 0 )
        self.button_StartCalibration.setEnabled( 0 )
        self.button_StopCalibration.setEnabled(  0 )

        # Layout
        layout = QGridLayout()

        layout.addWidget(IMUAccLabel1, 0, 0)
        layout.addWidget(self.IMUAccLabel2, 0, 1)
        layout.addWidget(self.IMUAccLabel3, 1, 1)

        layout.addWidget(IMUGyrLabel1, 2, 0)
        layout.addWidget(self.IMUGyrLabel2, 2, 1)
        layout.addWidget(self.IMUGyrLabel3, 3, 1)

        layout.addWidget(IMUMagLabel1, 4, 0)
        layout.addWidget(self.IMUMagLabel2, 4, 1)
        layout.addWidget(self.IMUMagLabel3, 5, 1)

        layout.addWidget(IMUMicLabel1, 6, 0)
        layout.addWidget(self.IMUMicLabel2, 6, 1)

        layout.addWidget(IMUSystemLabel1, 7, 0)
        layout.addWidget(self.IMUSystemLabel2, 7, 1)
    
        layout.addWidget(self.button_CheckStatus, 8, 0, 1, 2)
        layout.addWidget(self.button_StartCalibration, 9, 0)
        layout.addWidget(self.button_StopCalibration, 9, 1)
               
        # Group
        self.ImuGroup = QGroupBox( title )
        self.ImuGroup.setAlignment(QtCore.Qt.AlignCenter)
        self.ImuGroup.setStyleSheet("QGroupBox { font-weight: bold; } ")
        self.ImuGroup.setLayout( layout )

    # ----------------------------------------------------------

    def MotorsGroup(self, title):
        # Widgets
        MicroStepLabel = QLabel("Step Resolution:")
        self.radio1 = QRadioButton("Full")
        self.radio2 = QRadioButton("Half")
        self.radio4 = QRadioButton("Quarter")
        self.radio8 = QRadioButton("1/8")
        self.radio16 = QRadioButton("1/16")
        self.radio32 = QRadioButton("1/32")
        self.radio1.setChecked( True )
        self.radio2.setChecked( False )
        self.radio4.setChecked( False )
        self.radio8.setChecked( False )
        self.radio16.setChecked( False )
        self.radio32.setChecked( False )

        self.button_ApplyMotors = QPushButton( "Apply Settings" )
        icon1 = 'SP_DialogApplyButton'
        img1 = self.centralWidget.style().standardIcon(getattr(QStyle, icon1))
        self.button_ApplyMotors.setIcon( img1 )
        self.button_ApplyMotors.setEnabled( 0 )

        # Layout
        layout = QGridLayout()
        layout.addWidget(MicroStepLabel, 0, 0)
        layout.addWidget( self.radio1,  1, 0)
        layout.addWidget( self.radio2,  1, 1)
        layout.addWidget( self.radio4,  1, 2)
        layout.addWidget( self.radio8,  2, 0)
        layout.addWidget( self.radio16,  2, 1)
        layout.addWidget( self.radio32,  2, 2)
        layout.addWidget( self.button_ApplyMotors, 3, 0, 1, 3)
       
        # Group
        self.MotorsGroup = QGroupBox( title )
        self.MotorsGroup.setAlignment(QtCore.Qt.AlignCenter)
        self.MotorsGroup.setStyleSheet("QGroupBox { font-weight: bold; } ")
        self.MotorsGroup.setLayout( layout )
    # -------------------------------------

    def ScanGroup(self, title):
        # Widgets: Buttons: UI Actions
        self.button_StartScan = QPushButton( "Start" )
        self.button_PauseScan = QPushButton( "Pause" )
        self.button_StopScan  = QPushButton( "Stop"  )
        
        icon1 = 'SP_MediaPlay'
        icon3 = 'SP_DialogCancelButton'
        icon4 = 'SP_MediaPause'
        img1 = self.centralWidget.style().standardIcon(getattr(QStyle, icon1))
        img3 = self.centralWidget.style().standardIcon(getattr(QStyle, icon3))
        img4 = self.centralWidget.style().standardIcon(getattr(QStyle, icon4))

        self.button_StartScan.setIcon( img1 )
        self.button_PauseScan.setIcon( img4 )
        self.button_StopScan.setIcon(  img3 )

        self.button_StartScan.setEnabled( 0 )
        self.button_PauseScan.setEnabled( 0 )
        self.button_StopScan.setEnabled(  0 )

        # Widgets
        self.progressBar = QProgressBar()
        self.progressBar.setTextVisible( 1 )
        self.progressBar.setRange( 0, 100 )
        self.progressBar.setValue( 0 )
        #self.ui.progressBar.setMinimum( 0 )
        #self.ui.progressBar.setMaximum( 100 )
        # Layout
        layout = QGridLayout()
        layout.addWidget(self.button_StartScan,  0, 0)
        layout.addWidget(self.button_PauseScan,  0, 1)
        layout.addWidget(self.button_StopScan,   1, 0, 1, 2)
        layout.addWidget(self.progressBar,       2, 0, 1, 2)
        # Group
        self.ScanGroup = QGroupBox( title )
        self.ScanGroup.setAlignment(QtCore.Qt.AlignCenter)
        self.ScanGroup.setStyleSheet("QGroupBox { font-weight: bold; } ") 
        self.ScanGroup.setLayout( layout )

    def LogosGroup(self, title):
        path = os.path.dirname(os.path.abspath(__file__))
        self.IsepLogo = QLabel()
        pixmap = QtGui.QPixmap(os.path.join(path, 'img/isep.jpeg'))
        pixmap = pixmap.scaled(300, 150)
        self.IsepLogo.setPixmap(pixmap)
        
        self.DeeLogo = QLabel()
        pixmap = QtGui.QPixmap(os.path.join(path, 'img/DEE.jpg'))
        pixmap = pixmap.scaled(300, 150)
        self.DeeLogo.setPixmap(pixmap)
        
        # Layout
        layout = QGridLayout()
        layout.addWidget(self.IsepLogo,  0, 0)
        layout.addWidget(self.DeeLogo,  0, 1)

        # Group
        self.LogosGroup = QGroupBox()
        self.LogosGroup.setAlignment(QtCore.Qt.AlignCenter)
        self.LogosGroup.setStyleSheet("QGroupBox { font-weight: bold; } ") 
        self.LogosGroup.setLayout( layout )
# ===========================================================	
# EOF.

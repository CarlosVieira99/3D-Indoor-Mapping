"""
Module: SceneViewerAPP.py
@authors: Carlos Vinhais & Carlos Silva
cvinhais@gmail.com / 1160628@isep.ipp.pt
"""

import sys
import numpy as np
import vtk
import time
import socket
import threading
import serial
import datetime
from vtk.util.numpy_support import vtk_to_numpy
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
import struct
from PyQt5 import Qt, QtCore, QtGui, QtWidgets # QtCore, QtGui,
from PyQt5.QtWidgets import *
import SceneViewerGUI


""" A class for Scene Viewer APP """

class SceneViewerApp( QtWidgets.QMainWindow ):
 
    def __init__(self, parent=None):

        # Parent constructor
        super( SceneViewerApp, self).__init__()
        self.ui = SceneViewerGUI.Ui_MainWindow()
        self.ui.setupUi(self)

        # ========================================================
        self.APP_NAME    = "3D Indoor Mapping App"
        self.APP_VERSION = "v0"
        # ========================================================

        # APP Callbacks - "Menu -> File, Help"
        self.ui.FileSaveAction.triggered.connect(           self.File_Save_VTK )
        self.ui.FileExportAction.triggered.connect(         self.File_Export )
        self.ui.StatsSaveAction.triggered.connect(          self.File_Save_Stats )
        self.ui.AllSaveAction.triggered.connect(            self.File_Save_All )
        self.ui.FileQuitAction.triggered.connect(           self.File_Quit )

        self.ui.Button_Connect_COM.clicked.connect(         self.ConnectCOM )
        self.ui.Button_Disconnect_COM.clicked.connect(      self.DisconnectCOM )
        self.ui.button_CheckStatus.clicked.connect(         self.CheckStatus)
        self.ui.button_StartCalibration.clicked.connect(    self.StartCalibrate)
        self.ui.button_StopCalibration.clicked.connect(     self.StopCalibrate)
        self.ui.button_ApplyMotors.clicked.connect(         self.ApplyMotors)
        self.ui.button_StartScan.clicked.connect(           self.StartScan)
        self.ui.button_PauseScan.clicked.connect(           self.PauseScan)
        self.ui.button_StopScan.clicked.connect(            self.StopScan)
        self.ui.HelpAboutAction.triggered.connect(          self.Help_About )

        # Global Variables
        self.calibrateFlag = False
        self.PauseScanFlag = False
        self.StopScanFlag = False
        self.stepMode = 1
        self.ThreadClientFlag = False

        self.flag_STOP = False

        icon = 'SP_MediaPlay'
        self.imgMediaPlay = self.ui.centralWidget.style().standardIcon(getattr(QStyle, icon))
        icon = 'SP_MediaPause'
        self.imgMediaPause = self.ui.centralWidget.style().standardIcon(getattr(QStyle, icon))

        # ========================================================
        # Point Cloud
        # ========================================================
        self.points   = vtk.vtkPoints()
        self.vertices = vtk.vtkCellArray()
        self.vtkdepth = vtk.vtkDoubleArray()
        self.vtkdepth.SetNumberOfComponents(1)
        self.vtkdepth.SetName('vtkdepth')

        self.cloud = vtk.vtkPolyData()
        self.cloud.SetPoints( self.points )
        self.cloud.SetVerts( self.vertices )
        self.cloud.GetPointData().SetScalars(self.vtkdepth)
        self.cloud.GetPointData().SetActiveScalars('vtkdepth')

        self.mapper = vtk.vtkPolyDataMapper()
        self.mapper.SetInputData( self.cloud )
        #self.mapper.SetScalarRange(100, 12000)

        self.cloudActor = vtk.vtkActor()
        self.cloudActor.GetProperty().SetPointSize( 2 )
        self.cloudActor.SetMapper( self.mapper )

        self.ui.qvtk1.ren.AddActor( self.cloudActor )

        self.lineSource = vtk.vtkLineSource()
        self.lineSource.SetPoint1( 0,0,0 )
        self.lineSource.SetPoint2( 0,0,2 )
        self.lineSource.Update()

        self.beamMapper = vtk.vtkPolyDataMapper()
        self.beamMapper.SetInputConnection( self.lineSource.GetOutputPort() )

        self.beamActor = vtk.vtkActor()
        self.beamActor.GetProperty().SetEdgeColor( 1.0, 1.0, 1.0 )
        self.beamActor.GetProperty().SetLineWidth( 2 )

        self.beamActor.SetMapper( self.beamMapper )

        self.ui.qvtk1.ren.AddActor( self.beamActor )

        # ========================================================


    # ===========================================================
    # # General Functions
    # ===========================================================
    # ===========================================================
    # USB Send Message and Wait Answer
    # ===========================================================
    def USB_sendWaitAnswer(self, usb_obj, sendMessage, recvMesssage):
        data = " "
        usb_obj.write(sendMessage.encode())
        while data != recvMesssage:
            data = usb_obj.readline()[:-2] #the last bit gets rid of the new-line chars
            if data:
                data = data.decode()

    # ===========================================================
    # Start Server
    # ===========================================================
    def StartServer(self, SERVER, PORT):
        self.DISCONNECT_MESSAGE = '!DISCONNECT'
        ADDR   = (SERVER, PORT)

        try:
            self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        except socket.error as err:
            self.ui.statusBar.clearMessage()
            self.ui.statusBar.showMessage('Failed to create server socket!' + str(err))
            return False

        try:
            self.server.bind( ADDR )
        except Exception as err:
            self.ui.statusBar.clearMessage()
            self.ui.statusBar.showMessage('Error: PORT already in use! Please choose another one')
            return False

        self.server.listen()
        self.conn, self.addr = self.server.accept()
        print(f'[NEW CONNECTION] {self.addr}')
        print(f'[ACTIVE THREADS] {threading.active_count()}')
        return True

    # ===========================================================
    # Wifi Send Message
    # ===========================================================
    def WIFI_sendMessage(self, message):
        self.FORMAT = 'UTF-8'
        self.conn.sendall(bytes(message, self.FORMAT))

    # ===========================================================
    # Wifi Receive Message
    # ===========================================================
    def WIFI_recvMessage(self):
         data = self.conn.recv(1024).decode()
         return data

    # ===========================================================
    # Convert Seconds to Days, Hours, Minutes, Seconds
    # ===========================================================
    def SEC_TO_DHMS(self, tSeconds):
        days = tSeconds // (24 * 3600) 
        tSeconds = tSeconds % (24 * 3600) 
        hours= tSeconds // 3600
        tSeconds %= 3600
        minutes  = tSeconds // 60
        tSeconds %= 60
        seconds = tSeconds

        return days, hours, minutes, seconds

    # ===========================================================
    # Reset Scan
    # ===========================================================
    def ResetPointCloud( self  ):
        # self.ui.progressBar.setValue( 0 )
        # self.ui.qvtk1.CleanViewer()

        #Reset Point Cloud
        self.points   = vtk.vtkPoints()
        self.vertices = vtk.vtkCellArray()
        self.vtkdepth = vtk.vtkDoubleArray()

        self.cloud.SetPoints( self.points )
        self.cloud.SetVerts( self.vertices )
        self.cloud.GetPointData().SetScalars(self.vtkdepth)

        self.lineSource.SetPoint1( 0,0,0 )
        self.lineSource.SetPoint2( 0,0,5 )

        self.ui.qvtk1.iren.Render()

        # self.ui.qvtk1.ren.AddActor( self.cloudActor )
        # self.ui.qvtk1.ren.AddActor( self.beamActor )

    # ===========================================================
    # Reset Scan
    # ===========================================================
    def ResetScan(self):
        # self.ui.progressBar.setValue( 0 )
        # self.ui.qvtk1.CleanViewer()
        self.ResetPointCloud()
        # self.ui.qvtk1.ren.AddActor( self.cloudActor )
        # self.ui.qvtk1.ren.AddActor( self.beamActor )

    # ===========================================================
    # # APP Button Callbacks to Create Threads
    # ===========================================================
    def ConnectCOM(self):
        print(f'[ACTIVE THREADS] {threading.active_count()}')
        self.ConnectCOMthread = threading.Thread(target=self.ConnectCOMThread,
                                         args=(), daemon = True)
        self.ConnectCOMthread.start()

    
    def StartCalibrate(self):
        print(f'[ACTIVE THREADS] {threading.active_count()}')
        self.StartCalibratethread = threading.Thread(target=self.StartCalibrateThread,
                                         args=(), daemon = True)
        self.StartCalibratethread.start()
    
    
    def StartScan(self):
        print(f'[ACTIVE THREADS] {threading.active_count()}')
        self.StartScanthread = threading.Thread(target=self.StartScanThread,
                                         args=(self.ui.qvtk1.cornerAnnotation,), daemon = True)
        self.StartScanthread.start()

        self.ProgressBarthread = threading.Thread(target=self.ProgressBarThread,
                                        args=(), daemon = True)
        self.ProgressBarthread.start()
    
    # ===========================================================
    # # APP Button Callbacks
    # ===========================================================
    # ===========================================================
    # Disconnect Communications
    # ===========================================================
    def DisconnectCOM(self):
        self.WIFI_sendMessage(("D"))

        while True:
            data = self.conn.recv(32).decode()
            if(data == "DISCONNECTED"):
                self.conn.close()
                self.server.close()
                self.ThreadClientFlag = True
                self.ui.Label_STATUS2.setText("Disconnected")
                self.ui.Label_STATUS2.setStyleSheet("color: red")
                self.ui.Label_ScannerIP2.clear()
                self.ui.Label_ScannerIP2.setText("xxx.xxx.xxx.xxx")
                self.ui.Label_ScannerIP2.setStyleSheet("color: black")
                self.ui.Button_Disconnect_COM.setEnabled( 0 )
                self.ui.button_CheckStatus.setEnabled( 0 )
                self.ui.button_StartCalibration.setEnabled( 0 )
                self.ui.button_ApplyMotors.setEnabled( 0 )
                self.ui.button_StartScan.setEnabled( 0 )
                self.ui.button_StopScan.setEnabled( 0 )
                self.ui.button_PauseScan.setEnabled( 0 )
                self.ui.statusBar.clearMessage()
                self.ui.statusBar.showMessage("All disconnected")
                return

    # ===========================================================
    # Check IMU Status
    # ===========================================================
    def CheckStatus(self):
        self.WIFI_sendMessage("IS")
        while True:
            data = self.WIFI_recvMessage()
            self.WIFI_sendMessage("ACK")

            if data == 'ACC_OK':
                self.ui.IMUAccLabel2.setText("Ok")
                self.ui.IMUAccLabel2.setStyleSheet('color: green')
            elif data == 'ACC_NOK':
                self.ui.IMUAccLabel2.setText("ERROR!")
                self.ui.IMUAccLabel2.setStyleSheet('color: red')

            if data == 'MAG_OK':
                self.ui.IMUMagLabel2.setText("Ok")
                self.ui.IMUMagLabel2.setStyleSheet('color: green')
            elif data == 'MAG_NOK':
                self.ui.IMUMagLabel2.setText("ERROR!")
                self.ui.IMUMagLabel2.setStyleSheet('color: red')

            if data == 'GYR_OK':
                self.ui.IMUGyrLabel2.setText("Ok")
                self.ui.IMUGyrLabel2.setStyleSheet('color: green')
            elif data == 'GYR_NOK':
                self.ui.IMUGyrLabel2.setText("ERROR!")
                self.ui.IMUGyrLabel2.setStyleSheet('color: red')

            if data == 'MIC_OK':
                self.ui.IMUMicLabel2.setText("Ok")
                self.ui.IMUMicLabel2.setStyleSheet('color: green')
                return
            elif data == 'MIC_NOK':
                self.ui.IMUMicLabel2.setText("ERROR!")
                self.ui.IMUAMicLabel2.setStyleSheet('color: red')
                return
    
    # ===========================================================
    # Stop IMU Calibration
    # ===========================================================
    def StopCalibrate(self):
        self.calibrateFlag = True

        if(self.sys_calibration == 3):
            self.ui.IMUSystemLabel2.setText("Calibrated")
            self.ui.IMUSystemLabel2.setStyleSheet('color: green')
        else:
            self.ui.IMUSystemLabel2.setText("Uncalibrated")
            self.ui.IMUSystemLabel2.setStyleSheet('color: red')

        if(self.gyr_calibration == 3):
            self.ui.IMUGyrLabel3.setText("Calibrated")
            self.ui.IMUGyrLabel3.setStyleSheet('color: green')
        else:
            self.ui.IMUGyrLabel3.setText("Uncalibrated")
            self.ui.IMUGyrLabel3.setStyleSheet('color: red')

        if(self.acc_calibration == 3):
            self.ui.IMUAccLabel3.setText("Calibrated")
            self.ui.IMUAccLabel3.setStyleSheet('color: green')
        else:
            self.ui.IMUAccLabel3.setText("Uncalibrated")
            self.ui.IMUAccLabel3.setStyleSheet('color: red')

        if(self.mag_calibration == 3):
            self.ui.IMUMagLabel3.setText("Calibrated")
            self.ui.IMUMagLabel3.setStyleSheet('color: green')
        else:
            self.ui.IMUMagLabel3.setText("Uncalibrated")
            self.ui.IMUMagLabel3.setStyleSheet('color: red')

        self.ui.Button_Disconnect_COM.setEnabled( 1 )
        self.ui.button_CheckStatus.setEnabled( 1 )
        self.ui.button_StartCalibration.setEnabled( 1 )
        self.ui.button_StopCalibration.setEnabled( 0 )
        self.ui.button_ApplyMotors.setEnabled( 1 )

        self.WIFI_sendMessage("S")
        
        while True:
            data = self.WIFI_recvMessage()
            if(data == "END_CALIBRATE"):
                return

        self.ui.statusBar.clearMessage()
        self.ui.statusBar.showMessage("IMU Calibrated")


    # ===========================================================
    # Apply Motors Settings
    # ===========================================================
    def ApplyMotors(self):
        msg = "M"
        if self.ui.radio1.isChecked():
            msg = msg + "F"
            self.stepMode = 1
        elif self.ui.radio2.isChecked():
            msg = msg + "H"
            self.stepMode = 2
        elif self.ui.radio4.isChecked():
            msg = msg + "Q"
            self.stepMode = 4
        elif self.ui.radio8.isChecked():
            msg = msg + "E"
            self.stepMode = 8
        elif self.ui.radio16.isChecked():
            msg = msg + "S"
            self.stepMode = 16
        elif self.ui.radio32.isChecked():
            msg = msg + "T"
            self.stepMode = 32

        #corners.SetText(3, f"PPS: {'{:.2f}'.format(PPS)}" )
        #self.ui.qvtk1.cornerAnnotation.SetText(1, "sal")

        self.totalPoints = (self.stepMode**2) * 100 * 100 + self.stepMode*100
        self.WIFI_sendMessage(msg)


        while True:
            data = self.WIFI_recvMessage()
            if(data == "MOTORS_CHANGED"):
                self.ui.button_StartScan.setEnabled(1)
                return

    # ===========================================================
    # Pause Scan
    # ===========================================================
    def PauseScan(self):
        self.PauseScanFlag = not self.PauseScanFlag

        if(self.PauseScanFlag):
            self.ui.button_PauseScan.setText("Continue")
            self.ui.button_PauseScan.setIcon( self.imgMediaPlay )
            self.ui.button_StopScan.setEnabled( 1 )
        else:
            self.ui.button_PauseScan.setText("Pause")
            self.ui.button_PauseScan.setIcon( self.imgMediaPause )
            self.ui.button_StopScan.setEnabled( 0 )

    # ===========================================================
    # Stop Scan
    # ===========================================================
    def StopScan(self):
        self.StopScanFlag = True
        self.WIFI_sendMessage("S")

        while True:
            data = self.WIFI_recvMessage()
            if data:
                break

        self.ui.Button_Disconnect_COM.setEnabled(1)
        self.ui.Button_Disconnect_COM.setEnabled(1)
        self.ui.button_CheckStatus.setEnabled(1)
        self.ui.button_StartCalibration.setEnabled(1)
        self.ui.button_ApplyMotors.setEnabled(1)
        self.ui.button_StartScan.setEnabled(1)
        self.ui.button_PauseScan.setText("Pause")
        self.ui.button_PauseScan.setIcon( self.imgMediaPause )
        self.ui.button_PauseScan.setEnabled(0)
        self.ui.button_StopScan.setEnabled(0)
        self.ui.progressBar.setValue( 0 )
        self.ResetScan()
        self.PauseScanFlag = False

    # ===========================================================
    # APP Menu Bar Callbacks
    # ===========================================================
    # ===========================================================
    # File Quit
    # ===========================================================
    def File_Quit(self):  # QMessageBox.question
        self.ui.statusBar.showMessage('Quit?')
        # -----------------------------------------    
        buttonReply = QMessageBox.question(self,
                      'Scene Viewer APP', "Do you want to Quit?",
                      QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if buttonReply == QMessageBox.Yes:
            # self.Stop() # stop the thread if daemon = True?
            # self.hide() # hide main window ?
            sys.exit()
        else:
            pass
        # -----------------------------------------
        self.ui.statusBar.showMessage('Ready.')

    # ===========================================================
    # File Save
    # ===========================================================
    def File_Save_VTK(self):
        outputFilename = QtWidgets.QFileDialog.getSaveFileName( self,
                         'Save Point Cloud As...', 'cloud.vtk',
                         filter=('*.vtk'))[0]
        if ( outputFilename ):
            print ( "Writing:", outputFilename )
            writer = vtk.vtkPolyDataWriter()
            writer.SetInputData( self.cloud )
            writer.SetFileName( outputFilename )
            writer.Write()

    # ===========================================================
    # File Export
    # ===========================================================
    def File_Export(self):
        outputFilename = QtWidgets.QFileDialog.getSaveFileName( self,
                        'Export Screenshot As...', 'screenshot.png',
                        filter=('*.png'))[0]
        if ( outputFilename ):
            print ( "Writing:", outputFilename )
            windowToImageFilter = vtk.vtkWindowToImageFilter()
            windowToImageFilter.SetInput( self.ui.qvtk1.renWin )
            windowToImageFilter.Update()
            writer = vtk.vtkPNGWriter()
            writer.SetInputData( windowToImageFilter.GetOutput() )
            writer.SetFileName( outputFilename )
            writer.Write()

    # ===========================================================
    # File Save Statistics
    # ===========================================================
    def File_Save_Stats(self):
        outputFilename = QtWidgets.QFileDialog.getSaveFileName( self, 'Export statistic files as...')[0]
        if ( outputFilename ):
            print(outputFilename)
            points = self.cloud.GetPoints()
            pointsData = points.GetData()
            npts = points.GetNumberOfPoints()
            array3d = vtk_to_numpy(points.GetData())

            xPoints = array3d[:, 0]
            yPoints = array3d[:, 1]
            zPoints = array3d[:, 2]

            self.autocad_points(outputFilename, xPoints, yPoints, zPoints)
            self.autocad_lines(outputFilename, xPoints, yPoints, zPoints)
            self.file_xyz(outputFilename, xPoints, yPoints, zPoints)
            #self.statistics(outputFilename, npts, xPoints, yPoints, zPoints)
            with open(f"{outputFilename}_stats.txt", "w") as f:
                f.write(f"Begnning of the test at: {self.beginTestDate}\n")
                f.write(f"Test ended at: {self.endTestDate}\n")
                daysTimeElapsed, hoursTimeElapsed, minutesTimeElapsed, secondsTimeElapsed = self.SEC_TO_DHMS(self.endTimeElapsed - self.beginTimeElapsed)
                if(daysTimeElapsed > 0):
                    MessageStatus = f'Time Elapsed: {daysTimeElapsed}D {hoursTimeElapsed}H {minutesTimeElapsed}M {round(secondsTimeElapsed, 0)}S'
                elif (hoursTimeElapsed > 0):
                    MessageStatus = f'Time Elapsed: {hoursTimeElapsed}H {minutesTimeElapsed}M {round(secondsTimeElapsed, 0)}S'
                elif (minutesTimeElapsed > 0):
                    MessageStatus = f'Time Elapsed: {minutesTimeElapsed}M {round(secondsTimeElapsed, 0)}S'
                else:
                    MessageStatus = f'Time Elapsed: {round(secondsTimeElapsed, 0)}S'
                f.write(f"{MessageStatus}\n")
                f.write(f"Total Points: {npts}\n")
                f.write(f"Average PPS: {round((npts/(self.endTimeElapsed - self.beginTimeElapsed)), 2)}")

    def autocad_points(self, filename, x, y, z):
        with open(f'{filename}_points.scr', 'w') as f:
            f.write("_MULTIPLE _POINT\n")
            for i in range(len(x)):
                f.write(f"{x[i]},{y[i]},{z[i]}\n")

    def autocad_lines(self, filename, x, y, z):
        with open(f'{filename}_lines.scr', 'w') as f:
            f.write("._3DPOLY\n")
            for i in range(len(x)):
                f.write(f"{x[i]},{y[i]},{z[i]}\n")

    def file_xyz(self, filename, x, y, z):
        depth = np.sqrt(x**2 + y**2 + z**2)
        red = []
        green = []
        blue = []

        for i in range(len(depth)):
            if depth[i] <= 6000:
                red.append(255-0.0425*depth[i])
                green.append(0.0425*depth[i])
                blue.append(0)
            else:
                red.append(0)
                green.append(255-0.0425*(depth[i]-6000))
                blue.append(0.0425*(depth[i]-6000))
        
        with open(f'{filename}_pointsDepth.xyz', 'w') as f:
            for i in range(len(depth)):
                f.write(f"{x[i]} {y[i]} {z[i]} {red[i]} {green[i]} {blue[i]}\n")

    def statistics(self, filename, nPoints, x, y, z):
        rad_r = []
        widthPlot = []
        zeroIndex = []

        zeroIndex.append(0)
        self.stepMode = 2

        for i in range(1, int(10100/100)*2*self.stepMode-3, 2):
            zeroIndex.append(zeroIndex[i-1]+100*self.stepMode)
            zeroIndex.append(zeroIndex[i]+1)

        zeroIndex.append(10100*self.stepMode-1)
        zeroIndex = np.array(zeroIndex)
        
        
        # Descobrir pontos da planta
        for i in range(len(z)-1):
            if(i in zeroIndex):
                radian = np.arctan2(y[i], x[i])
                distance = np.sqrt(x[i]**2 + y[i]**2)
                if((x[i] >= 0) and (y[i] >= 0)):
                    radian = radian
                elif((x[i] <= 0) and (y[i] >= 0)):
                    radian = radian
                elif((x[i] <= 0) and (y[i] <= 0)):
                    radian = radian + 2*np.pi
                elif((x[i] >= 0) and (y[i] <= 0)):
                    radian = radian + 2*np.pi

                rad_r.append([radian, distance])

        rad_r = sorted(rad_r,key=lambda x: x[0]) # Afinal não é preciso fazer sort
        rad2 = [i[0] for i in rad_r]
        rad2.append(rad2[-1]+rad2[1])
        rad2.pop(0)
        r2 = [i[1] for i in rad_r]
        r2.append(r2[0])
        r2.pop(0)

        rad2 = np.array(rad2)
        r2 = np.array(r2)

        rad_mid = (rad2[:-1] + rad2[1:])/2 # Midpoints
        r_mid = (r2[:-1] + r2[1:])/2

        r2 = r2/1000
        r_mid = r_mid/1000

        for i in range(len(rad2)-1):
            widthPlot.append(rad2[i+1]-rad2[i]) # Constante

        plt.polar(rad_mid, r_mid,'bo-', color="blue", markersize=2)
        ax = plt.subplot(111, projection='polar', label="blueprint")
        ax.bar(rad_mid, r_mid, width=widthPlot, bottom=0.0, align='edge', alpha=0.5, color='b', linewidth=0)
        ax.set_title("Blue print", loc="left")
        ax.legend(["Distance (m)"], loc="best")

        dx = widthPlot[0]


        distTotal = []
        distIdx = []
        dist = []
        for i in range(len(x)):
            distTotal.append(np.sqrt(x[i]**2 + y[i]**2 + z[i]**2))

        for i in range(int(100*self.stepMode)):
            distIdx.append((100*self.stepMode)*i+50*self.stepMode)
    
        for i in range(len(distIdx)):
            dist.append(distTotal[distIdx[i]])
        dist = np.array(dist) / 1000

        ###############################################
        ############# Calculus ( mean, media, std, var)
        N = len(dist)
        # Precisão // Precision (diferença entre os valores medidos / Consistencia)
        t_student = 1
        r_medio     = np.mean(dist)
        desvio_pad  = np.std(dist)
        variancia   = np.var(dist)
        incerteza_abs  = t_student * desvio_pad / (np.sqrt(N)) # Standard Error
        incerteza_rel   = incerteza_abs/r_medio

        mostD = np.max(r2)
        if mostD < 6.000:
            mostDerror = 0.06
        else:
            mostDerror = mostD*0.01

        hpoint = np.max(z, axis=0)/1000
        hpointIdx = np.argmax(z, axis=0)
        hpointDist = np.sqrt(x[hpointIdx]**2 + y[hpointIdx]**2 + z[hpointIdx]**2)/1000
        hpointRadian = np.arcsin(hpoint/hpointDist)
        if hpointDist < 6.000:
            hpointError = (hpointDist+0.06)*np.sin(hpointRadian) - hpoint
        else:
            hpointError = (hpointDist+hpointDist*0.01)*np.sin(hpointRadian) - hpoint

        rError = []
        for i in range(len(r2)):
            if r2[i] < 6.000:
                rError.append(r2[i]+0.06)
            else:
                rError.append(r2[i]+r2[i]*0.01)
        rError = np.array(rError)

        triangleRiemannSum = np.sum(0.5 * r2 * r2*np.tan(dx)) #0.5 * b * h
        triangleRiemannSumMax = np.sum(0.5 * rError * rError*np.tan(dx))
        triangleRiemannSumError = triangleRiemannSumMax - triangleRiemannSum
        
        CircleRiemannSum = np.sum(np.pi * r2**2 * dx/(2*np.pi)) #pi*r^2
        CircleRiemannSumMax = np.sum(np.pi * rError**2 * dx/(2*np.pi)) #pi*r^2
        CircleRiemannSumMaxError = CircleRiemannSumMax - CircleRiemannSum
        
        trianglePerimeter = np.sum(r2*np.tan(dx))
        trianglePerimeterMax = np.sum(rError*np.tan(dx))
        trianglePerimeterError = trianglePerimeterMax - trianglePerimeter
        
        circlePerimeter = np.sum(2*np.pi*r2*(dx/(2*np.pi)))
        circlePerimeterMax = np.sum(2*np.pi*rError*(dx/(2*np.pi)))
        circlePerimeterError = circlePerimeterMax - circlePerimeter
        

        with open(f"{filename}_stats.txt", "w") as f:
            f.write(f"Begnning of the test at: {self.beginTestDate}\n")
            f.write(f"Test ended at: {self.endTestDate}\n")

            daysTimeElapsed, hoursTimeElapsed, minutesTimeElapsed, secondsTimeElapsed = self.SEC_TO_DHMS(self.endTimeElapsed - self.beginTimeElapsed)
            if(daysTimeElapsed > 0):
                MessageStatus = f'Time Elapsed: {daysTimeElapsed}D {hoursTimeElapsed}H {minutesTimeElapsed}M {round(secondsTimeElapsed, 0)}S'
            elif (hoursTimeElapsed > 0):
                MessageStatus = f'Time Elapsed: {hoursTimeElapsed}H {minutesTimeElapsed}M {round(secondsTimeElapsed, 0)}S'
            elif (minutesTimeElapsed > 0):
                MessageStatus = f'Time Elapsed: {minutesTimeElapsed}M {round(secondsTimeElapsed, 0)}S'
            else:
                MessageStatus = f'Time Elapsed: {round(secondsTimeElapsed, 0)}S'

            f.write(f"{MessageStatus}\n")
            f.write(f"Step Mode: {self.stepMode}\n")
            f.write(f"Total Points: {nPoints}\n")
            f.write(f"Average PPS: {round((nPoints/(self.endTimeElapsed - self.beginTimeElapsed)), 2)}\n")
            f.write(f"Absolute precision of north pole: +- {round(incerteza_abs, 3)} m\n")
            f.write(f"Relative precision of north pole: +- {round(incerteza_rel*100, 3)} %\n")
            f.write(f"Most distant point: {round(mostD, 3)} +- {round(mostDerror, 3)} m\n")
            f.write(f"Maximum height: {round(hpoint, 3)} +- {round(hpointError, 3)} m\n")
            f.write(f"Triangles Rienmann Sum Area: {round(triangleRiemannSum, 3)} +- {round(triangleRiemannSumError, 3)} m²\n")
            f.write(f"Circles Rienmann Sum Area: {round(CircleRiemannSum, 3)} +- {round(CircleRiemannSumMaxError, 3)} m²\n")
            f.write(f"Triangles Rienmann Sum Perimeter: {round(trianglePerimeter, 3)} +- {round(trianglePerimeterError, 3) } m\n")
            f.write(f"Circles Rienmann Sum Perimeter: {round(circlePerimeter, 3)} +- {round(circlePerimeterError, 3)} m")

        plt.savefig(f"{filename}_blueprint.png")

    # ===========================================================
    # File Save All
    # ===========================================================
    def File_Save_All(self):
        outputFilename = QtWidgets.QFileDialog.getSaveFileName( self, 'Export statistic files as...')[0]

        if ( outputFilename ):
            print(outputFilename)
            points = self.cloud.GetPoints()
            pointsData = points.GetData()
            npts = points.GetNumberOfPoints()
            array3d = vtk_to_numpy(points.GetData())

        with open(f"{outputFilename}_stats.txt", "w") as f:
            f.write(f"Begnning of the test at: {self.beginTestDate}\n")
            f.write(f"Test ended at: {self.endTestDate}\n")
            daysTimeElapsed, hoursTimeElapsed, minutesTimeElapsed, secondsTimeElapsed = self.SEC_TO_DHMS(self.endTimeElapsed - self.beginTimeElapsed)
            if(daysTimeElapsed > 0):
                MessageStatus = f'Time Elapsed: {daysTimeElapsed}D {hoursTimeElapsed}H {minutesTimeElapsed}M {round(secondsTimeElapsed, 0)}S'
            elif (hoursTimeElapsed > 0):
                MessageStatus = f'Time Elapsed: {hoursTimeElapsed}H {minutesTimeElapsed}M {round(secondsTimeElapsed, 0)}S'
            elif (minutesTimeElapsed > 0):
                MessageStatus = f'Time Elapsed: {minutesTimeElapsed}M {round(secondsTimeElapsed, 0)}S'
            else:
                MessageStatus = f'Time Elapsed: {round(secondsTimeElapsed, 0)}S'
            f.write(f"{MessageStatus}\n")
            f.write(f"Total Points: {npts}\n")
            f.write(f"Average PPS: {round((npts/(self.endTimeElapsed - self.beginTimeElapsed)), 2)}")

    # ===========================================================
    # Help About
    # ===========================================================
    def Help_About(self): # QMessageBox.information
        self.ui.statusBar.showMessage('About...')
        # -----------------------------------------
        message = self.APP_NAME + ' ' + str( self.APP_VERSION ) + '\n\n'
        message += "This software has the goal of doing a 3D of indoor spaces\n"
        message += 'CVS & CAV @ 2020' + '\n'
        QtWidgets.QMessageBox.information(QtWidgets.QWidget(), 'About', message)
        # ----------------------------------------- 
        self.ui.statusBar.showMessage('Ready.')
    
    # ===========================================================
    # # Threads
    # ===========================================================
    # ===========================================================
    # Connect Communications Thread
    # ===========================================================
    
    def ConnectCOMThread(self):
        self.ui.Label_STATUS2.setText("Connecting...")
        self.ui.Label_STATUS2.setStyleSheet('color: orange')

        usb_port  = str(self.ui.lineEdit_USBPort.text())
        wifi_ssid = str(self.ui.lineEdit_SSID.text())
        wifi_pwd  = str(self.ui.lineEdit_PWD.text())
        wifi_host = str(self.ui.lineEdit_HOST.text())
        wifi_port = str(self.ui.lineEdit_PORT.text())

        try:
            esp32_usb = serial.Serial(usb_port, 115200, timeout=.1)
            # esp32_usb = serial.Serial('COM3', 115200, timeout=10)
            print ('connected OK!')
        except Exception as error:
            self.ui.statusBar.clearMessage()
            self.ui.statusBar.showMessage("Couldn't connect to " + usb_port)
            self.ui.Label_STATUS2.setText("Disconnected")
            self.ui.Label_STATUS2.setStyleSheet('color: red')
            return

        time.sleep(1) #give the connection a second to settle

        self.USB_sendWaitAnswer(esp32_usb, wifi_ssid, "SSID_OK")
        self.USB_sendWaitAnswer(esp32_usb, wifi_pwd,  "PWD_OK")
        self.USB_sendWaitAnswer(esp32_usb, wifi_host, "HOST_OK")
        self.USB_sendWaitAnswer(esp32_usb, wifi_port, "PORT_OK")

        while True:
            data = esp32_usb.readline()[:-2] #the last bit gets rid of the new-line chars
            if data:
                data = data.decode()
            if data == "CONNECTION_OK":
                break
            elif data == "CONNECTION_NOK":
                self.ui.statusBar.showMessage("SSID or Password Incorrect, please try again")
                self.ui.Label_STATUS2.setText("Disconnected")
                self.ui.Label_STATUS2.setStyleSheet('color: red')
                return

        if(not self.StartServer(wifi_host, int(wifi_port))):
            return

        data = " "
        scanner_ip= " "
        
        while True:
            data = esp32_usb.readline()[:-2].decode() #the last bit gets rid of the new-line chars
            if data:
                scanner_ip = data
                break

        while True:
            data = esp32_usb.readline()[:-2].decode() #the last bit gets rid of the new-line chars
            if data:
                data = data
            if data == "CONNECTION_OK":
                break
            elif data == "CONNECTION_NOK":
                self.ui.Label_STATUS2.setText("Disconnected")
                self.ui.Label_STATUS2.setStyleSheet('color: red')
                return

        esp32_usb.close()

        self.ui.statusBar.clearMessage()
        self.ui.statusBar.showMessage("Connected ")
  
        self.ui.Label_STATUS2.setText("Connected")
        self.ui.Label_STATUS2.setStyleSheet('color: green')
        self.ui.Label_ScannerIP2.setText(scanner_ip)
        self.ui.Label_ScannerIP2.setStyleSheet('color: blue')
        self.ui.Button_Connect_COM.setEnabled( 0 )
        self.ui.Button_Disconnect_COM.setEnabled( 1 )
        self.ui.button_CheckStatus.setEnabled( 1 )
        self.ui.button_StartCalibration.setEnabled( 1 )
        self.ui.button_ApplyMotors.setEnabled( 1 )

    # ===========================================================
    # Start IMU Calibration
    # ===========================================================
    def StartCalibrateThread(self):
        self.WIFI_sendMessage("IC")
        self.ui.Button_Disconnect_COM.setEnabled( 0 )
        self.ui.button_CheckStatus.setEnabled( 0 )
        self.ui.button_StartCalibration.setEnabled( 0 )
        self.ui.button_StopCalibration.setEnabled( 1 )
        self.ui.button_ApplyMotors.setEnabled( 0 )

        while True:
            data = self.WIFI_recvMessage()
            if(self.calibrateFlag):
                self.calibrateFlag = False
                return
            if data == "END_CALIBRATE":
                return
            else:
                data = data.split(" ")

            self.sys_calibration = int(data[0])
            self.gyr_calibration = int(data[1])
            self.acc_calibration = int(data[2])
            self.mag_calibration = int(data[3])

            statusMessage  = " System: "        + str(self.sys_calibration)
            statusMessage += " Gyroscope: "     + str(self.gyr_calibration)
            statusMessage += " Accelerometer: " + str(self.acc_calibration)
            statusMessage += " Magnetometer: "  + str(self.mag_calibration)

            self.ui.statusBar.clearMessage()
            self.ui.statusBar.showMessage(statusMessage)
            self.WIFI_sendMessage("ACK")

    # ===========================================================
    # Start Scan Thread
    # ===========================================================
    def StartScanThread(self, corners):
        self.ResetScan()
        self.ui.Button_Disconnect_COM.setEnabled( 0 )
        self.ui.button_CheckStatus.setEnabled( 0 )
        self.ui.button_StartCalibration.setEnabled( 0 )
        self.ui.button_ApplyMotors.setEnabled( 0 )
        self.ui.button_StartScan.setEnabled( 0 )
        self.ui.button_PauseScan.setEnabled( 1 )
        self.ui.button_StopScan.setEnabled( 0 )
        self.StopScanFlag = False

        distAntes = 100

        PPS = 0
        self.beginTestDate = str(datetime.datetime.now())

        self.WIFI_sendMessage("S")

        self.beginTimeElapsed = time.time()
        counterPPS=0
        beginPPS = time.time()

        f = open('scan1.txt', 'w')

        while True:
            while(self.PauseScanFlag):
                time.sleep(0.1) # Improves performance
                if(self.StopScanFlag):
                    return

            corners.SetText(2, f"Total Points: {self.cloud.GetNumberOfPoints()}" )
            corners.SetText(1, str(datetime.datetime.now()))
            self.ui.qvtk1.ren.AddViewProp( self.ui.qvtk1.cornerAnnotation ) # It does not refresh without this

            data = self.WIFI_recvMessage()
            self.WIFI_sendMessage("ACK")

            if(data == "END_SCAN"):
                PPS = self.cloud.GetNumberOfPoints() / (time.time()- self.beginTimeElapsed)
                corners.SetText(3, f"PPS: {'{:.2f}'.format(PPS)}" )
                f.close()
                self.endTestDate = str(datetime.datetime.now())
                self.ui.qvtk1.iren.Render() 
                self.ui.Button_Disconnect_COM.setEnabled(1)
                self.ui.button_CheckStatus.setEnabled(1)
                self.ui.button_StartCalibration.setEnabled(1)
                self.ui.button_ApplyMotors.setEnabled(1)
                self.ui.button_StartScan.setEnabled(1)
                self.ui.button_PauseScan.setEnabled( 0 )
                self.PauseScanFlag = True
                self.StopScanFlag = True
                return
    
            f.write(f"{data}\n")
            data = data.split(" ")
            millis      = float(data[0])
            theta       = float(data[1])
            phi         = float(data[2])
            dist        = float(data[3])
            strenght    = float(data[4])
            celsius     = float(data[5])
            q0          = float(data[6])
            q1          = float(data[7])
            q2          = float(data[8])
            q3          = float(data[9])

            #print(phi)

            #dist = dist*10

            if(dist>12000 or dist<100):
                dist = distAntes
            else:
                distAntes = dist

            x = dist*np.cos(phi)*np.cos(theta)
            y = dist*np.cos(phi)*np.sin(theta)
            z = dist*np.sin(phi)

            point = [x, y, z]

            counterPPS = counterPPS+1
            
            # add new point (3 floats), cell point and data
            pid = self.points.InsertNextPoint( point )
            self.vertices.InsertNextCell(1)
            self.vertices.InsertCellPoint(pid)
            self.vtkdepth.InsertNextValue( dist/12000 )

            # update cloud polydata
            self.points.Modified()
            self.vertices.Modified()
            self.vtkdepth.Modified()
            self.cloud.Modified()

            # update line
            self.lineSource.SetPoint2( point )

            if(counterPPS == 20):
                endPPS = time.time()
                newPPS = counterPPS / (endPPS-beginPPS)
                
                # Low Pass Filter
                PPS = PPS*0.90 + newPPS*0.10

                corners.SetText(3, f"PPS: {'{:.2f}'.format(PPS)}" )
                corners.SetText(0, f"Step Mode: 1/{self.stepMode}")
                counterPPS = 0
                beginPPS = time.time()

                self.endTimeElapsed = time.time()
                TimeElapsed = int(self.endTimeElapsed - self.beginTimeElapsed)

                daysTimeElapsed, hoursTimeElapsed, minutesTimeElapsed, secondsTimeElapsed = self.SEC_TO_DHMS(TimeElapsed)

                if(daysTimeElapsed > 0):
                    MessageStatus = f'Time Elapsed: {daysTimeElapsed}D {hoursTimeElapsed}H {minutesTimeElapsed}M {secondsTimeElapsed}S'
                elif (hoursTimeElapsed > 0):
                    MessageStatus = f'Time Elapsed: {hoursTimeElapsed}H {minutesTimeElapsed}M {secondsTimeElapsed}S'
                elif (minutesTimeElapsed > 0):
                    MessageStatus = f'Time Elapsed: {minutesTimeElapsed}M {secondsTimeElapsed}S' 
                else:
                    MessageStatus = f'Time Elapsed: {secondsTimeElapsed}S'

                PointsLeft = self.totalPoints - self.cloud.GetNumberOfPoints()
                TimeLeft = int(PointsLeft / PPS)

                daysTimeLeft, hoursTimeLeft, minutesTimeLeft, secondsTimeLeft = self.SEC_TO_DHMS(TimeLeft)

                if(daysTimeLeft > 0):
                    MessageStatus += f' Time Left: {daysTimeLeft}D {hoursTimeLeft}H {minutesTimeLeft}M {secondsTimeLeft}S'
                elif (hoursTimeLeft > 0):
                    MessageStatus += f' Time Left: {hoursTimeLeft}H {minutesTimeLeft}M {secondsTimeLeft}S'
                elif (minutesTimeLeft > 0):
                    MessageStatus += f' Time Left: {minutesTimeLeft}M {secondsTimeLeft}S' 
                else:
                    MessageStatus += f' Time Left: {secondsTimeLeft}S'

                self.ui.SetMessageStatus(MessageStatus)

            # update vtk rendering
            self.ui.qvtk1.iren.Render()

    # ===========================================================
    # Progress Bar Thread
    # ===========================================================
    def ProgressBarThread(self):
        while True:
            while(self.PauseScanFlag):
                time.sleep(0.1) # Improves performance
                if(self.StopScanFlag):
                    return

            nPoints = self.cloud.GetNumberOfPoints()
            progress = 100*nPoints/self.totalPoints
            self.ui.progressBar.setValue( progress )
            if(progress == 100):
                return

# ===============================================
if __name__ == "__main__": 
    app = Qt.QApplication(sys.argv)
    myapp = SceneViewerApp()
    myapp.show()
    sys.exit(app.exec_())
    # app.quit()
# ===============================================

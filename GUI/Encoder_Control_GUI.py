# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Encoder_Control_GUI.ui'
#
# Created by: PyQt5 UI code generator 5.14.1
#
# WARNING! All changes made in this file will be lost!
# -------------------------------------------------------------------------
# This code has been developped by: William Bonilla
# For any questions you can contact my at WilliamBonilla@protonmail.com
# ********************************************************************
# Before starting to update the software please read the Readme file.
# ********************************************************************
# -------------------------------------------------------------------------
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QMessageBox
from lib.Encoder_Control_GUI_ONLY import Ui_Tester

import time
import sys

import os

# import configparser as ConfigParser  # Python 3
from lib import configFile
from lib import saveData
from lib.plotData import PlotData
from lib.MplCanvas import MplCanvas

from api_phidget_n_MQTT.src.lib_api_phidget22 import phidget22Handler as handler
from api_phidget_n_MQTT.src.lib_global_python import MQTT_client

class Ui_Encoder(Ui_Tester):
    def setupUi(self, Tester):
        super().setupUi(Tester)

        self.newWidgets(Tester)

        # import config file could depending on the name of the config file
        file = 'config.cfg'
        self.config = configFile.configFile(configFilename=file)

        self.retranslateUiNew(Tester,self.config.configuration())
        QtCore.QMetaObject.connectSlotsByName(Tester)
        # Ends of the GUI Widget init------------------------------------------------------------------------------------------

        # Init GUI default values
        self.urlRepo.setOpenExternalLinks(True)
        # Minimum value of the SpinBox which correspond to the minimum of interval time 8ms
        minValueDataInt = self.config.configuration().getint('encoder','minValueDataInt')
        # Maximum value of the SpinBox which correspond to the maximum of interval time 1000ms
        maxValueDataInt = self.config.configuration().getint('encoder','maxValueDataInt')
        # Set range of the SpinBox
        self.DataIntervalSpinBox.setRange(minValueDataInt, maxValueDataInt)
        # Set displayed value from saved one in config
        self.DataIntervalSpinBox.setValue(self.config.configuration().getint('encoder','datainterval'))
        # Default text of filename
        self.textEditFile.setPlainText(self.config.configuration().get('filenameLogger','filename_default'))
        # Default text of Directory
        self.textEditDirectory.setPlainText(self.config.configuration().get('filenameLogger','folderpath_default'))
        # Recording slider range
        self.RecordingEnco.setRange(0, 100)


        # Init of the encodeur
        self.encoderWthMQTT = handler.encoderWthMQTT(self.config.configuration())
        self.clientLogger = None
        connectionStatus = False
        guiReady = True
        self.distance = 0
        self.saveData=saveData.saveData()
        self.isRecordData = False
        self.lastDisplay = time.time()

        # User interaction----------------------------------------------------------------------------------------------
        # This blocks links all the functions with all interaction possible between the user and the GUI.
        self.connectWidgets()
        
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.displayMeasuresLCD)

        self.timerStatusBar = QtCore.QTimer()
        self.timerStatusBar.timeout.connect(self.messageStatusBar)
        self.updateStatusBar()

    def newWidgets(self,Tester):
        pass

    def initMenuBar(self):
        pass

    def connectWidgets(self):
        self.CloseButton.clicked.connect(self.closeEvent)
        self.RegisterEnco.stateChanged.connect(self.Savedata)
        self.DisplayPlotButton.clicked.connect(self.PlotData)
        self.FileConfirmButton.clicked.connect(self.NewFile)
        self.DirectoryConfirmB.clicked.connect(self.NewPath)
        self.ToConnectButton.clicked.connect(self.ConnectToEnco)
        self.ToDisconnectButton.clicked.connect(self.DisconnectEnco)
        self.DataIntervalButton.clicked.connect(self.SetDataInterval)
        self.ToResetDistance.clicked.connect(self.ResetDistance)

        self.actionStyle.triggered.connect(self.dialogStyle)
        self.actionStyleDefault.triggered.connect(self.styleDefault)

        pass

        
    def updateStatusBar(self):
        self.satusBarCount = [0,0]
        if self.timerStatusBar.isActive():
            self.timerStatusBar.stop()

        self.statusDataInterval= str(self.config.configuration().getint('encoder','datainterval'))
        try:
            self.statusFile = os.path.basename(self.saveData.fh.name)
        except:
            self.statusFile = self.config.configuration().get('filenameLogger','filename')
        self.statusFolder = self.config.configuration().get('filenameLogger','folderpath')
        self.timerStatusBar.start(300)

    def messageStatusBar(self):
        msg_length=30

        if len(self.statusFile)>msg_length or len(self.statusFolder)>msg_length:
            self.statusBar.showMessage("Data interval : "+self.statusDataInterval+"ms"+" | "
                                        +"file : "+self.statusFile[self.satusBarCount[0]:msg_length+self.satusBarCount[0]]+" | "
                                        +"folder : "+self.statusFolder[self.satusBarCount[1]:msg_length+self.satusBarCount[1]])
            self.satusBarCount[0]+=1
            self.satusBarCount[1]+=1
            
            if self.satusBarCount[0]+msg_length-10 >= len(self.statusFile):
                self.satusBarCount[0] = 0
            if self.satusBarCount[1]+msg_length-10 >= len(self.statusFolder):
                self.satusBarCount[1] = 0
        else:
            self.statusBar.showMessage("Data interval : "+self.statusDataInterval+"ms"+" | "
                                        +"file : "+self.statusFile[self.satusBarCount[0]:msg_length+self.satusBarCount[0]]+" | "
                                        +"folder : "+self.statusFolder[self.satusBarCount[1]:msg_length+self.satusBarCount[1]])

    def centerOnScreen(self):
        qtRectangle = self.frameGeometry()
        centerPoint = QDesktopWidget().availableGeometry().center()
        qtRectangle.moveCenter(centerPoint)
        self.move(qtRectangle.topLeft())

    # All coded actions
    # Functions without arguments--------------------------------------------------------------------------------------
    # This functions creates a message box to make the user wants to quit the GUI.
    def closeEvent(self, event):
        reply = QMessageBox.question(self.CloseButton, 'Quit?', 'Are you sure you want to quit?', QMessageBox.Yes | QMessageBox.No,
                                     QMessageBox.No)
        if reply == QMessageBox.Yes:
            if not type(event) == bool:
                event.accept()
            else:
                sys.exit()
        else:
            if not type(event) == bool:
                event.ignore()

    # Create a messagebox when the registring starts or is done
    def registerIsOnMessage(self):
        if self.RegisterEnco.isChecked():
            self.informationMessageBox("Information recording","Recording has started")
        else:
            self.informationMessageBox("Information recording","Recording is finished")

    def ConnectToEnco(self):
        self.encoderWthMQTT.ConnectToEnco(self.config.configuration())
        if self.encoderWthMQTT.isConnected:
            self.connectionSucces()
            self.timer.start(0)
            self.lastDisplay = time.time()
        else:
            self.connectionFail()

    def DisconnectEnco(self):
        try:
            self.encoderWthMQTT.DisconnectEnco()
            self.timer.stop()
            self.disconnectedEnco()
        except:
            self.informationMessageBox("Encoder","Disconnection failed")
            pass

    def informationMessageBox(self,title,text):
        FailedFileMessage = QMessageBox()
        FailedFileMessage.setIcon(QMessageBox.Information)
        FailedFileMessage.setWindowTitle(title)
        FailedFileMessage.setText(text)
        FailedFileMessage.setStandardButtons(QMessageBox.Ok)
        FailedFileMessage.exec_()

    def warningMessageBox(self,title,text):
        FailedFileMessage = QMessageBox()
        FailedFileMessage.setIcon(QMessageBox.Warning)
        FailedFileMessage.setWindowTitle(title)
        FailedFileMessage.setText(text)
        FailedFileMessage.setStandardButtons(QMessageBox.Ok)
        FailedFileMessage.exec_()

    def connectionSucces(self):
        self.informationMessageBox("Encoder","Connection succeed")

    def disconnectedEnco(self):
        self.informationMessageBox("Encoder","disconnection succeed")

    def connectionFail(self):
        self.warningMessageBox("Encoder","Connection failed")

    def FailedFile(self):
        self.informationMessageBox("Error","Unable to find file")

    def NewFile(self):
        self.config.NewFile(self.textEditFile.toPlainText())
        self.updateStatusBar()

    def NewPath(self):
        self.config.NewPath(self.textEditDirectory.toPlainText())
        self.updateStatusBar()

    def SetDataInterval(self):
        self.config.SetDataInterval(self.DataIntervalSpinBox.value())
        self.updateStatusBar()

    def PlotData(self):
        if not PlotData(self.config.configuration()):
            self.FailedFile()

    def Savedata(self):
        try:
            if not self.clientLogger and self.RecordingEnco.value() == 0:
                self.clientLogger = MQTT_client.createClient(None, self.config.configuration())
        except:
            self.clientLogger = None

        if self.clientLogger:
            self.RecordingEnco.setValue(self.saveData.saveDataMQTT(self.clientLogger, self.config.configuration(), self.updateStatus()))
        else:
            self.RecordingEnco.setValue(self.saveData.saveDataSimple(self.config.configuration(),self.updateStatus()))
            if self.RecordingEnco.value() ==0:
                # self.timer2.stop()
                self.isRecordData = False
                pass
            else:
                print("***record started***")
                self.isRecordData = True
                # self.timer2.start(0)
                pass
        #     self.RecordingEnco.setValue(self.saveData.Savedata(self.encoderWthMQTT, self.config.configuration(), self.updateStatus()))

        self.registerIsOnMessage()

    def recordData(self):
        self.saveData.onMessage(self.encoderWthMQTT)
        self.encoderWthMQTT.event_obj_onPositionChange.clear()

    def displayMeasuresLCD(self):
        self.lcdDistance.display(self.encoderWthMQTT.distance / 100) #distance in mm
        self.lcdDistance.repaint()
        
        if self.encoderWthMQTT.event_obj_onPositionChange.wait(0.1):
            if self.isRecordData and self.encoderWthMQTT.isConnected:
                self.recordData()
                pass
            else:
                pass

            if time.time() - self.lastDisplay >= 0.3:
                self.lcdTimeRecording.display(self.encoderWthMQTT.t1)
                self.lcdTimeRecording.repaint()
                self.lcdPositionChange.display(self.encoderWthMQTT.positionChange)
                self.lcdPositionChange.repaint()
                self.lcdTimeChange.display(self.encoderWthMQTT.timeChange)
                self.lcdTimeChange.repaint()

                if self.RecordingEnco.value() == 0:
                    self.encoderWthMQTT.event_obj_onPositionChange.clear()

                self.lastDisplay = time.time()
                # time.sleep(0.3)
        else:
            pass

    def ResetDistance(self):
        self.encoderWthMQTT.ResetDistance()

    def updateStatus(self):
        if self.RegisterEnco.isChecked():
            return True
        else:
            return False

    

    # Adds all the title to the object on the GUI
    # For renaming the objects you do it instead of going trough QT

    def retranslateUiNew(self, Tester, config):
        _translate = QtCore.QCoreApplication.translate
        # Tester.setWindowTitle(_translate("Tester", "Interface de contrôle"))
        # self.groupBox_2.setTitle(_translate("Tester", "Encoder"))
        # self.RegisterEnco.setText(_translate("Tester", "Enregistrement"))
        # self.groupBox_5.setTitle(_translate("Tester", "Connectivité"))
        # self.ToConnectButton.setText(_translate("Tester", "Connexion"))
        # self.ToDisconnectButton.setText(_translate("Tester", "Déconnexion"))
        # self.DisplayPlotButton.setText(_translate("Tester", "Graphique"))
        # self.DisplayData_2.setText(_translate("Tester", "Reset distance"))
        # self.textBoxDirectory.setText(_translate("Tester", "Dossier"))
        # self.DirectoryConfirmB.setText(_translate("Tester", "Confirmer"))
        # self.textBoxFile.setText(_translate("Tester", "Fichier"))
        # self.FileConfirmButton.setText(_translate("Tester", "Confirmer"))
        # self.textBoxDataInterval.setText(_translate("Tester", "Data Interval"))
        # self.DataIntervalButton.setText(_translate("Tester", "Confirmer"))
        # self.CloseButton.setText(_translate("Tester", "Fermer"))
        # self.groupBox_3.setTitle(_translate("Tester", "Afficher données"))
        # self.lcdTextTimeRecording.setText(_translate("Tester", "Time recording [s]"))
        # self.lcdTextPositionChange.setText(_translate("Tester", "Position Change"))
        # self.lcdTextTimeChange.setText(_translate("Tester", "Time change [ms]"))
        # self.lcdTextDistance.setText(_translate("Tester", "Distance [dm]"))

        try:
            repoAdress=config.get('REPO','GitHub')
        except:
            repoAdress='https://github.com/WilliamBonilla62/GUIPythonEncodeur/'
        hrefRepoAdress=f'<a href="{repoAdress}">{repoAdress}</a>'
        self.urlRepo.setText(_translate("Tester",hrefRepoAdress))

if __name__ == "__main__":
    # Make sure current path is this file path
    abspath = os.path.abspath(__file__)
    dname = os.path.dirname(abspath)
    os.chdir(dname)

    app = QtWidgets.QApplication(sys.argv)
    Tester = QtWidgets.QMainWindow()
   
    ui = Ui_Encoder()
    ui.setupUi(Tester)
    Tester.show() # normal window size
    Tester.showMaximized() # Toggle fullscreen at start
    sys.exit(app.exec_())

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
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtWidgets import *
from Phidget22.Devices.Encoder import *
from Phidget22.Devices.Log import *
from Phidget22.LogLevel import *
from Phidget22.PhidgetException import *

import traceback
import time
import sys

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches

import os

# sys.path.append("/home/pi/Documents/api_phidget_n_MQTT_2/src/lib_api_phidget22")
# import phidget22Handler as handler

# import configparser as ConfigParser  # Python 3
import configFile

from api_phidget_n_MQTT.src.lib_api_phidget22 import phidget22Handler as handler
from api_phidget_n_MQTT.src.lib_global_python import searchLoggerFile
from api_phidget_n_MQTT.src.lib_global_python import createLoggerFile
from api_phidget_n_MQTT.src.lib_global_python import loggerHandler
from api_phidget_n_MQTT.src.lib_global_python import MQTT_client

# -----------------------------------------------------------------------------
def ConnectToEnco(client, config, encoder0):
    ############
    # connection to Phidget encoder and wait for measures
    # publish the datas on config/MQTT/topic
    try:
        Log.enable(LogLevel.PHIDGET_LOG_INFO, "phidgetlog.log")
        # Create your Phidget channels
        # Set addressing parameters to specify
        encoder0.client = client
        # encoder0.clientTopic = config.get('MQTT', 'topic')
        encoder0.clientTopic = config.get('encoder', 'topic_publish')
        encoder0.printLog = config.getboolean('encoder', 'printLog')
        encoder0.chooseDataInterval = config.getint('encoder', 'dataInterval')

        # Assign any event handlers you need before calling open so that no events are missed.
        encoder0.setOnPositionChangeHandler(handler.onPositionChange)
        encoder0.setOnAttachHandler(handler.onAttach)
        encoder0.setOnDetachHandler(handler.onDetach)
        # Open your Phidgets and wait for attachment
        encoder0.openWaitForAttachment(5000)
        ui.connectionSucces()
    except PhidgetException as ex:
        ui.connectionFail()
        # We will catch Phidget Exceptions here, and print the error informaiton.
        traceback.print_exc()
        print("")
        print("PhidgetException " + str(ex.code) + " (" + ex.description + "): " + ex.details)


def DisconnectEnco(encoder0):
    encoder0.close()
    encoder0.client.loop_stop()
    ui.disconnectedEnco()


def PlotData(config):
    ############
    # Encoder's resolution in mm per pulse
    #     Encoder_mm_per_Pulse = 0.02
    Encoder_mm_per_Pulse = config.getfloat('encoder', 'resolution')
    print("encoder resolution : " + str(Encoder_mm_per_Pulse))

    ############
    # search for the last logger file based on the indentation
    #     filename="Logger_encoder_07.txt"
    filename = searchLoggerFile.searchLoggerFile(config)
    try:
        data = np.genfromtxt(filename, delimiter=",", names=True)
    except:
        ui.FailedFile()
        return
    # convert the number of pulse position change into mm
    PositionChange_mm = data['PositionChange'] * Encoder_mm_per_Pulse

    # recorded time when datas are received in s
    time = data['TimeRecording']
    time -= time[0]  # the beginning time at 0

    # vel is the velocity measured by the encoder
    # as the positionChange_mm is in mm and the TimeChange is in ms
    # the velocity is given in m/s
    # If a 'detach' from the encoder, TimeChange=0 and vel will be Inf
    vel = np.divide(PositionChange_mm, data['TimeChange'])

    ############
    # initialize the plot
    fig, ax1 = plt.subplots()

    # plot the encoder velocity in time
    color = 'tab:blue'
    lns1 = ax1.plot(time, vel, label="Velocity", color=color)
    ax1.set_xlabel("time[s]")
    ax1.set_ylabel("Velocity[m/s]", color=color)

    color = 'tab:blue'
    ax1.tick_params(axis='y', labelcolor=color)
    ax1.grid()

    #     # Create a Rectangle patch
    #     rect = patches.Rectangle((0,0),20,0.2,linewidth=1,edgecolor='k',facecolor='tab:grey')
    #     # Add the patch to the Axes
    #     ax1.add_patch(rect)

    # Draw a grey rectangle patch for each detach of the encoder aka 'missing values' aka TimeChange=0
    for k in np.argwhere(data['TimeChange'] == 0):
        if k == 0:
            rect = patches.Rectangle((time[k], 0), time[k + 1] - time[k], 2, linewidth=1, edgecolor='k',
                                     facecolor='tab:grey')
            ax1.add_patch(rect)
            lns3 = rect
        elif k != len(data['TimeChange']):
            if k == np.argwhere(data['TimeChange'] == 0)[0]:
                rect = patches.Rectangle((time[k - 1], 0), time[k + 1] - time[k - 1], 2, linewidth=1, edgecolor='k',
                                         facecolor='tab:grey')
                lns3 = ax1.add_patch(rect)
            else:
                rect = patches.Rectangle((time[k - 1], 0), time[k + 1] - time[k - 1], 2, linewidth=1, edgecolor='k',
                                         facecolor='tab:grey')
                ax1.add_patch(rect)

    # plot the encoder distance measured in m
    ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis

    color = 'tab:red'
    ax2.set_ylabel('Position[m]', color=color)  # we already handled the x-label with ax1
    lns2 = ax2.plot(time, np.cumsum(PositionChange_mm / 1000), color=color, label="Position")
    ax2.tick_params(axis='y', labelcolor=color)

    plt.title("velocity and position measured by encoder \n in file : " + filename)

    # Legend manage if there is no missing value meaning lns3 does not exist
    try:
        lns = [lns1[0], lns2[0], lns3]
        labs = ('Velocity', 'Position', 'Missing velocity')
    except:
        lns = [lns1[0], lns2[0]]
        labs = ('Velocity', 'Position')
    ax1.legend(lns, labs)  # , loc=0)

    fig.tight_layout()  # otherwise the right y-label is slightly clipped
    plt.show()


def Savedata(client, config, isChecked):
    if isChecked:

        fh = createLoggerFile.createLoggerFile(config)
        client.fh = fh
        client.printLog = config.getboolean('Logger', 'printLog')
        client.firstLine = config.get('filenameLogger', 'firstLine')
        client.saveLog = config.getboolean('Logger', 'saveLog')

        client.on_message = loggerHandler.on_message
        client.loop_start()

        # topic_encoder = config.get('MQTT', 'topic')
        topic_encoder = config.get('encoder', 'topic_subscribe')
        client.subscribe(topic_encoder)
        ui.RecordingEnco.setValue(100)
    #         try:
    #             input("Press Enter to Stop\n")
    #         except (Exception, KeyboardInterrupt):
    #             print("Logger encoder stopped !")
    #         finally:
    #             #stop the loop
    #             client.loop_stop()
    #             #fh.close()
    else:
        client.loop_stop()
        client.fh.close()
        ui.RecordingEnco.setValue(0)
    ui.registerIsOnMessage()
class Ui_Tester(QWidget):
    def setupUi(self, Tester):
        Tester.setObjectName("Tester")
        Tester.resize(673, 541)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("../../Downloads/Cirris.ico"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        Tester.setWindowIcon(icon)
        self.centralwidget = QtWidgets.QWidget(Tester)
        self.centralwidget.setObjectName("centralwidget")
        self.groupBox_2 = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox_2.setGeometry(QtCore.QRect(200, 0, 191, 80))
        self.groupBox_2.setObjectName("groupBox_2")
        self.RecordingEnco = QtWidgets.QSlider(self.groupBox_2)
        self.RecordingEnco.setGeometry(QtCore.QRect(10, 30, 160, 16))
        self.RecordingEnco.setOrientation(QtCore.Qt.Horizontal)
        self.RecordingEnco.setObjectName("RecordingEnco")
        self.RegisterEnco = QtWidgets.QCheckBox(self.groupBox_2)
        self.RegisterEnco.setGeometry(QtCore.QRect(10, 50, 141, 23))
        self.RegisterEnco.setObjectName("RegisterEnco")
        self.CloseButton = QtWidgets.QPushButton(self.centralwidget)
        self.CloseButton.setGeometry(QtCore.QRect(580, 470, 89, 25))
        self.CloseButton.setObjectName("CloseButton")
        self.groupBox_3 = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox_3.setGeometry(QtCore.QRect(10, 0, 181, 441))
        self.groupBox_3.setObjectName("groupBox_3")
        self.DisplayPlotButton = QtWidgets.QPushButton(self.groupBox_3)
        self.DisplayPlotButton.setGeometry(QtCore.QRect(10, 400, 161, 25))
        self.DisplayPlotButton.setObjectName("DisplayPlotButton")
        self.lcdTimeRecording = QtWidgets.QLCDNumber(self.groupBox_3)
        self.lcdTimeRecording.setGeometry(QtCore.QRect(10, 40, 141, 51))
        self.lcdTimeRecording.setObjectName("lcdTimeRecording")
        self.label_3 = QtWidgets.QLabel(self.groupBox_3)
        self.label_3.setGeometry(QtCore.QRect(10, 90, 161, 17))
        self.label_3.setObjectName("label_3")
        self.lcdPositionChange = QtWidgets.QLCDNumber(self.groupBox_3)
        self.lcdPositionChange.setGeometry(QtCore.QRect(10, 110, 141, 51))
        self.lcdPositionChange.setObjectName("lcdPositionChange")
        self.label_4 = QtWidgets.QLabel(self.groupBox_3)
        self.label_4.setGeometry(QtCore.QRect(10, 160, 161, 17))
        self.label_4.setObjectName("label_4")
        self.lcdTimeChange = QtWidgets.QLCDNumber(self.groupBox_3)
        self.lcdTimeChange.setGeometry(QtCore.QRect(10, 180, 141, 51))
        self.lcdTimeChange.setObjectName("lcdTimeChange")
        self.lcdIndexTriggered = QtWidgets.QLCDNumber(self.groupBox_3)
        self.lcdIndexTriggered.setGeometry(QtCore.QRect(10, 250, 141, 51))
        self.lcdIndexTriggered.setObjectName("lcdIndexTriggered")
        self.label_5 = QtWidgets.QLabel(self.groupBox_3)
        self.label_5.setGeometry(QtCore.QRect(10, 230, 161, 17))
        self.label_5.setObjectName("label_5")
        self.label_6 = QtWidgets.QLabel(self.groupBox_3)
        self.label_6.setGeometry(QtCore.QRect(10, 300, 161, 17))
        self.label_6.setObjectName("label_6")
        self.DisplayData = QtWidgets.QPushButton(self.groupBox_3)
        self.DisplayData.setGeometry(QtCore.QRect(10, 340, 161, 25))
        self.DisplayData.setObjectName("DisplayData")
        self.groupBox_4 = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox_4.setGeometry(QtCore.QRect(400, 0, 271, 401))
        self.groupBox_4.setObjectName("groupBox_4")
        self.textEditFile = QtWidgets.QTextEdit(self.groupBox_4)
        self.textEditFile.setGeometry(QtCore.QRect(10, 50, 251, 70))
        self.textEditFile.setObjectName("textEditFile")
        self.label = QtWidgets.QLabel(self.groupBox_4)
        self.label.setGeometry(QtCore.QRect(10, 30, 67, 17))
        self.label.setObjectName("label")
        self.FileConfirmButton = QtWidgets.QPushButton(self.groupBox_4)
        self.FileConfirmButton.setGeometry(QtCore.QRect(10, 130, 251, 25))
        self.FileConfirmButton.setObjectName("FileConfirmButton")
        self.textEditDirectory = QtWidgets.QTextEdit(self.groupBox_4)
        self.textEditDirectory.setGeometry(QtCore.QRect(10, 200, 251, 70))
        self.textEditDirectory.setObjectName("textEditDirectory")
        self.DirectoryConfirmB = QtWidgets.QPushButton(self.groupBox_4)
        self.DirectoryConfirmB.setGeometry(QtCore.QRect(10, 280, 251, 25))
        self.DirectoryConfirmB.setObjectName("DirectoryConfirmB")
        self.label_2 = QtWidgets.QLabel(self.groupBox_4)
        self.label_2.setGeometry(QtCore.QRect(10, 180, 67, 17))
        self.label_2.setObjectName("label_2")
        self.spinBox = QtWidgets.QSpinBox(self.groupBox_4)
        self.spinBox.setGeometry(QtCore.QRect(10, 330, 251, 26))
        self.spinBox.setObjectName("spinBox")
        self.label_7 = QtWidgets.QLabel(self.groupBox_4)
        self.label_7.setGeometry(QtCore.QRect(10, 310, 131, 17))
        self.label_7.setObjectName("label_7")
        self.DataIntervalButton = QtWidgets.QPushButton(self.groupBox_4)
        self.DataIntervalButton.setGeometry(QtCore.QRect(10, 360, 251, 25))
        self.DataIntervalButton.setObjectName("DataIntervalButton")
        self.groupBox_5 = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox_5.setGeometry(QtCore.QRect(200, 100, 191, 111))
        self.groupBox_5.setObjectName("groupBox_5")
        self.ToConnectButton = QtWidgets.QPushButton(self.groupBox_5)
        self.ToConnectButton.setGeometry(QtCore.QRect(10, 30, 171, 31))
        self.ToConnectButton.setObjectName("ToConnectButton")
        self.ToDisconnectButton = QtWidgets.QPushButton(self.groupBox_5)
        self.ToDisconnectButton.setGeometry(QtCore.QRect(10, 70, 171, 31))
        self.ToDisconnectButton.setObjectName("ToDisconnectButton")
        self.label_8 = QtWidgets.QLabel(self.centralwidget)
        self.label_8.setOpenExternalLinks(True)
        self.label_8.setGeometry(QtCore.QRect(10, 480, 441, 17))
        self.label_8.setObjectName("label_8")
        Tester.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(Tester)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 673, 22))
        self.menubar.setObjectName("menubar")
        Tester.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(Tester)
        self.statusbar.setObjectName("statusbar")
        Tester.setStatusBar(self.statusbar)

        # import config file could depending on the name of the config file
        file = 'config.cfg'
        config = configFile.configFile(configFilename=file)
        # config = ConfigParser.ConfigParser()
        # print("opening configuration file : config.cfg")
        # config.read(file)

        self.retranslateUi(Tester,config.configuration())
        QtCore.QMetaObject.connectSlotsByName(Tester)

        # Ends of the GUI init------------------------------------------------------------------------------------------
        self.label_8.setOpenExternalLinks(True)
        # Minimum value of the SpinBox which correspond to the minimum of interval time 8ms
        minValueDataInt = 8
        # Maximum value of the SpinBox which correspond to the maximum of interval time 1000ms
        maxValueDataInt = 1000
        # Init of the encodeur
        encoder0 = Encoder()
        connectionStatus = False
        guiReady = True
        clientLogger = MQTT_client.createClient("LoggerEncoder", config.configuration())
        clientEncoder = MQTT_client.createClient("Encoder", config.configuration())
        self.RecordingEnco.setRange(0, 100)
        self.textEditFile.setPlainText("Measures_")
        self.textEditDirectory.setPlainText("./save_measures/")
        if not os.path.exists("save_measures"):
            os.makedirs('save_measures')
        # User interaction----------------------------------------------------------------------------------------------
        # This blocks links all the functions with all interaction possible between the user and the GUI.
        self.CloseButton.clicked.connect(self.closeEvent)
        self.RegisterEnco.stateChanged.connect(lambda: Savedata(clientLogger, config.configuration(), self.updateStatus()))
        self.DisplayPlotButton.clicked.connect(lambda: PlotData(config.configuration()))
        # self.FileConfirmButton.clicked.connect(lambda: NewFile(file, config.configuration(), self.textEditFile.toPlainText()))
        self.FileConfirmButton.clicked.connect(lambda: config.NewFile(self.textEditFile.toPlainText()))
        # self.DirectoryConfirmB.clicked.connect(lambda: NewPath(file, config.configuration(), self.textEditDirectory.toPlainText()))
        self.DirectoryConfirmB.clicked.connect(lambda: config.NewPath(self.textEditDirectory.toPlainText()))
        self.ToConnectButton.clicked.connect(lambda: ConnectToEnco(clientEncoder, config.configuration(), encoder0))
        self.ToDisconnectButton.clicked.connect(lambda: DisconnectEnco(self, encoder0))
        self.spinBox.setRange(minValueDataInt, maxValueDataInt)
        # self.DataIntervalButton.clicked.connect(lambda: SetDataInterval(file, config.configuration(), self.spinBox.value()))
        self.DataIntervalButton.clicked.connect(lambda: config.SetDataInterval(self.spinBox.value()))
        self.DisplayData.clicked.connect(self.TestLCD)

    def centerOnScreen(self):
        qtRectangle = self.frameGeometry()
        centerPoint = QDesktopWidget().availableGeometry().center()
        qtRectangle.moveCenter(centerPoint)
        self.move(qtRectangle.topLeft())

    # All coded actions
    # Functions without arguments--------------------------------------------------------------------------------------
    # This functions creates a message box to make the user wants to quit the GUI.
    def closeEvent(self, event):
        reply = QMessageBox.question(self, 'Quit?', 'Are you sure you want to quit?', QMessageBox.Yes | QMessageBox.No,
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
            recordIsOn = QMessageBox()
            recordIsOn.setIcon(QMessageBox.Information)
            recordIsOn.setText("Recording has started")
            recordIsOn.setWindowTitle("Information recording")
            recordIsOn.setStandardButtons(QMessageBox.Ok)
            recordIsOn.exec_()
        else:
            recordIsOff = QMessageBox()
            recordIsOff.setIcon(QMessageBox.Information)
            recordIsOff.setText("Recording is done")
            recordIsOff.setWindowTitle("Information recording")
            recordIsOff.setStandardButtons(QMessageBox.Ok)
            recordIsOff.exec_()

    def connectionSucces(self):
        connectionIsSucces = QMessageBox()
        connectionIsSucces.setIcon(QMessageBox.Information)
        connectionIsSucces.setText("Connection succed")
        connectionIsSucces.setWindowTitle("Encoder")
        connectionIsSucces.setStandardButtons(QMessageBox.Ok)
        connectionIsSucces.exec_()

    def connectionFail(self):
        connectionIsFailed = QMessageBox()
        connectionIsFailed.setIcon(QMessageBox.Warning)
        connectionIsFailed.setText("Connection failed")
        connectionIsFailed.setWindowTitle("Encoder")
        connectionIsFailed.setStandardButtons(QMessageBox.Ok)
        connectionIsFailed.exec_()

    def disconnectedEnco(self):
        disconnected = QMessageBox()
        disconnected.setIcon(QMessageBox.Information)
        disconnected.setText("Connection failed")
        disconnected.setWindowTitle("Encoder")
        disconnected.setStandardButtons(QMessageBox.Ok)
        disconnected.exec_()

    def FailedFile(self):
        FailedFileMessage = QMessageBox()
        FailedFileMessage.setIcon(QMessageBox.Information)
        FailedFileMessage.setWindowTitle("Error")
        FailedFileMessage.setText("Unable to find file")
        FailedFileMessage.setStandardButtons(QMessageBox.Ok)
        FailedFileMessage.exec_()

    def TestLCD(self):
        dataFromFile = np.genfromtxt("Logger_encoder_gel_1cm_v1_00.txt", delimiter=",", names=True)
        t1 = dataFromFile["TimeRecording"]
        positionChange = dataFromFile["PositionChange"]
        timeChange = dataFromFile["TimeChange"]
        indexTriggered = dataFromFile["IndexTriggered"]

        for i in range(0, len(dataFromFile["TimeRecording"]), 1):
            self.lcdTimeRecording.display(t1[i])
            self.lcdTimeRecording.repaint()
            self.lcdPositionChange.display(positionChange[i])
            self.lcdPositionChange.repaint()
            self.lcdTimeChange.display(timeChange[i])
            self.lcdTimeChange.repaint()
            self.lcdIndexTriggered.display(indexTriggered[i])
            self.lcdIndexTriggered.repaint()
            time.sleep(0.3)

    def updateStatus(self):
        if self.RegisterEnco.isChecked():
            return True
        else:
            return False

    # Adds all the title to the object on the GUI
    # For renaming the objects you do it instead of going trough QT

    def retranslateUi(self, Tester, config):
        _translate = QtCore.QCoreApplication.translate
        Tester.setWindowTitle(_translate("Tester", "Interface de contrôle"))
        self.groupBox_2.setTitle(_translate("Tester", "Encoder"))
        self.RegisterEnco.setText(_translate("Tester", "Enregistrement"))
        self.CloseButton.setText(_translate("Tester", "Fermer"))
        self.groupBox_3.setTitle(_translate("Tester", "Afficher données"))
        self.DisplayPlotButton.setText(_translate("Tester", "Graphique de donnée"))
        self.label_3.setText(_translate("Tester", "Time recording"))
        self.label_4.setText(_translate("Tester", "Position Change"))
        self.label_5.setText(_translate("Tester", "Time change"))
        self.label_6.setText(_translate("Tester", "Index Triggered"))
        self.DisplayData.setText(_translate("Tester", "Afficher données"))
        self.groupBox_4.setTitle(_translate("Tester", "Fichier"))
        self.label.setText(_translate("Tester", "Fichier"))
        self.FileConfirmButton.setText(_translate("Tester", "Confirmer"))
        self.DirectoryConfirmB.setText(_translate("Tester", "Confirmer"))
        self.label_2.setText(_translate("Tester", "Dossier"))
        self.label_7.setText(_translate("Tester", "Data Interval"))
        self.DataIntervalButton.setText(_translate("Tester", "Confirmer"))
        self.groupBox_5.setTitle(_translate("Tester", "Connectivité"))
        self.ToConnectButton.setText(_translate("Tester", "Lancer connexion"))
        self.ToDisconnectButton.setText(_translate("Tester", "Déconnexion"))

        try:
            repoAdress=config.get('REPO','GitHub')
        except:
            repoAdress='https://github.com/WilliamBonilla62/GUIPythonEncodeur/'
        hrefRepoAdress=f'<a href="{repoAdress}">{repoAdress}</a>'
        self.label_8.setText(_translate("Tester",hrefRepoAdress))

if __name__ == "__main__":
    # Make sure current path is this file path
    abspath = os.path.abspath(__file__)
    dname = os.path.dirname(abspath)
    os.chdir(dname)

    app = QtWidgets.QApplication(sys.argv)
    Tester = QtWidgets.QMainWindow()
    ui = Ui_Tester()
    ui.setupUi(Tester)
    Tester.show()
    sys.exit(app.exec_())

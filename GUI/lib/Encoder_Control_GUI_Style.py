# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Encoder_Control_GUI_ONLY_modif_RP.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.

# fortement inspiré de: https://www.youtube.com/watch?v=Fk1TBoBcrR4&list=LL7klEEqnwSAUvihtsM3fGtg à plusieurs reprises,
# de https://www.mfitzp.com/tutorials/plotting-matplotlib/
# et de https://programtalk.com/python-examples/PyQt5.QtGui.QDesktopServices.openUrl/
# inspiré de https://stackoverflow.com/questions/60563477/pyqt5-tabwidget-tab-bar-blank-area-background-color

from PyQt5 import QtCore, QtGui, QtWidgets
from matplotlib.figure import Figure

from Encoder_Control_GUI_ONLY import Ui_Tester

import configFile
from MplCanvas import MplCanvas

import os

class Ui_Style(Ui_Tester):

    def dialogStyle(self):
        styleFont, choix = QtWidgets.QFontDialog.getFont()
        if choix:
            self.styleFont = styleFont
        else:
            return

        if not type(self.colorText)==type(QtGui.QColor()):
            Tester.setFont(self.styleFont)
        else:
            self.updateColorTester()

    def styleDefault(self):
        self.styleFont = QtGui.QFont("shelldlg2", 8)
        if not type(self.colorText)==type(QtGui.QColor()):
            Tester.setFont(self.styleFont)
        else:
            self.updateColorTester()

    def uncheckColorModeAll(self):
        for action in self.menuCouleur.actions():
            action.setChecked(False)

    def checkOneColorMode(self,actionName):
        self.uncheckColorModeAll()
        for x in self.menuCouleur.actions():
            if x.objectName() == actionName:
                action = x
        action.setChecked(True)

    def modeSombre(self):
        self.colorBackground = "rgb(43,43,43)"
        self.colorText = QtGui.QColor.fromRgb(255,255,255)#"rgb(255,255,255)"
        self.colorTabWidget = "rgb(30,30,30)"
        self.colorButton = "rgb(30,30,30)"
        self.colorMenuBar = "rgb(30,30,30)"

        self.colorTabWidget="rgb(63,63,63)"

        self.colorTabsDefault = "rgb(30,30,30)"
        self.colorTabSelected = "rgb(63,63,63)"
        self.colorTabHover = "blue"

        self.updateColor()
        self.checkOneColorMode("actionMode_sombre")


    def modeClair(self):
        self.colorBackground = "rgb(235,235,235)"
        self.colorText = QtGui.QColor.fromRgb(0,0,0)#"rgb(0,0,0)"
        self.colorTabWidget = "rgb(255,255,255)"
        self.colorButton = "rgb(200,200,200)"
        self.colorMenuBar = "rgb(255,255,255)"

        self.colorTabWidget="rgb(255,255,255)"

        self.colorTabsDefault ="rgb(235,235,235)"
        self.colorTabSelected ="rgb(255,255,255)"
        self.colorTabHover ="blue"

        self.updateColor()
        self.checkOneColorMode("actionMode_clair")

    def choixCouleurBackground(self):
        Qcolor = QtWidgets.QColorDialog.getColor()
        if not Qcolor.isValid():
            return
        color=Qcolor.name()

        self.colorBackground = color

        self.colorTabWidget = color
        self.colorButton = color
        self.colorMenuBar = color

        self.colorTabWidget = color

        self.colorTabsDefault = color
        self.colorTabSelected = color
        self.colorTabHover = "blue"
        self.updateColor()
        self.uncheckColorModeAll()

    def choixCouleurText(self):
        QcolorText = QtWidgets.QColorDialog.getColor()
        if not QcolorText.isValid():
            return
        self.colorText = QcolorText
        self.updateColorTester()
        self.updateColorTabText()
        self.uncheckColorModeAll()
        #Fonctions génériques sur les couleurs

    def updateColor(self):
        self.updateColorTester()
        self.updateColorTabWidget()
        self.updateColorMenuBar()
        self.updateColorButton()

    def updateColorTester(self):
        Tester.setStyleSheet("background-color:" + self.colorBackground + ";")

        if type(self.colorText)==type(QtGui.QColor()):
            self.centralwidget.setStyleSheet("color:" + self.colorText.name()+";"+
            "font-size:"+str(self.styleFont.pointSize())+"pt"+";"+
             "font-family:"+ self.styleFont.family()+";")

    def updateColorTabText(self):
        if type(self.colorText)==type(QtGui.QColor()):
            for x in range(len(self.tabWidget.children()[0].children())):
                    self.tabWidget.tabBar().setTabTextColor(x, self.colorText)
        else:
            pass

    def updateColorTabWidget(self):
        for x in self.tabWidget.children()[0].children():
            try:
                x.setStyleSheet("background-color:"+self.colorTabWidget+";")
            except:
                pass

        self.updateColorTabText()

        styleStr = str('''
                QTabBar::tab {{
                    background: {0};
                }}
                QTabBar::tab:selected {{
                    color: red;
                    background: {1};
                }}
                 QTabBar::tab:hover {{
                    color: white;
                    background-color: {3};
                }}
                '''.format(self.colorTabsDefault, self.colorTabSelected, self.colorText, self.colorTabHover))
        self.tabWidget.setStyleSheet(styleStr)


    def updateColorMenuBar(self):

        styleStr = str('''
                                 QMenuBar {{
                                    background-color: {0};
                                    color: {1};
                                    }}
                                QMenu {{
                                    background-color: {0};
                                    color: {1};
                                }}
                                 QMenu::item:selected {{
                                    background: blue;
                                    color: white
                                }}
                                '''.format(self.colorMenuBar, self.colorText.name()))


        #self.menuBar.setStyleSheet("background:" + self.colorMenuBar + ";")
        self.menuBar.setStyleSheet(styleStr)


    def updateColorButton(self):

        styleStr = str('''
                         QPushButton {{
                            background-color: {0};
                        }}
                         QPushButton::hover {{
                            background-color: blue;
                        }}
                        '''.format(self.colorButton))

        self.DirectoryConfirmB.setStyleSheet(styleStr)
        self.FileConfirmButton.setStyleSheet(styleStr)
        self.DataIntervalButton.setStyleSheet(styleStr)
        self.CloseButton.setStyleSheet(styleStr)
        self.DisplayPlotButton.setStyleSheet(styleStr)
        self.ToConnectButton.setStyleSheet(styleStr)
        self.ToDisconnectButton.setStyleSheet(styleStr)
        self.ToResetDistance.setStyleSheet(styleStr)

    def indexPropos(self):
        self.tabWidget.setCurrentIndex(3)

    def openRepo(self):
        try:
            repoAdress = self.config.configuration().get('REPO', 'GitHub')
        except:
            repoAdress = 'https://github.com/WilliamBonilla62/GUIPythonEncodeur/'
        QtGui.QDesktopServices.openUrl(QtCore.QUrl(repoAdress))

    def PlotData(self):
        self.graphic.figure.clf()
        self.graphic.axes = self.graphic.figure.add_subplot(111)
        self.graphic.axes2 = self.graphic.axes.twinx()

        self.updateGraphique()

        self.graphic.draw()

    def updateGraphique(self):
        import random
        self.graphic.axes.plot([0, 1, 2, 3, 4, 5, 6, 7],
                          [random.random(), random.random(), random.random(), random.random(), random.random(),
                           random.random(), random.random(), random.random()])

        self.graphic.axes2.plot([0, 1, 2, 3, 4, 5, 6, 7],
                    [random.random(), random.random(), random.random(), random.random(), random.random(),
                    random.random(), random.random(), random.random()],color='tab:red')


    def updateRemerciement(self):
        self.Liste.insertItem(0, "Adrien Pajon")
        self.Liste.insertItem(1, "Raymond-Pierre Bouchard")
        self.Liste.insertItem(2, "William Ricardo Bonilla Villatero")


    def setupUi(self, Tester):
        super().setupUi(Tester)

        self.colorBackground = ""
        self.colorText = QtGui.QColor.fromRgb(0,0,0)
        self.colorTabWidget = ""
        self.colorButton = ""
        self.colorMenuBar = ""
        self.styleFont = QtGui.QFont("shelldlg2", 8)

        self.labelRemerciements = QtWidgets.QLabel ( "Remerciements:" )
        self.verticalLayout_5.addWidget(self.labelRemerciements)
        self.Liste = QtWidgets.QListWidget()
        self.updateRemerciement()
        self.verticalLayout_5.addWidget(self.Liste)

        self.actionStyle = QtWidgets.QAction ( Tester )
        self.actionStyle.setCheckable(False)
        self.actionStyle.setObjectName("actionStyle")
        self.actionStyle.setShortcut("CTRL+M")
        self.actionStyle.setText("Modifier le style")

        self.actionStyleDefault = QtWidgets.QAction ( Tester )
        self.actionStyleDefault.setCheckable(False)
        self.actionStyleDefault.setObjectName("actionStyleDefault")
        self.actionStyleDefault.setShortcut("CTRL+D")
        self.actionStyleDefault.setText("Style par défaut")

        self.actionPaletteBackground = QtWidgets.QAction ( Tester )
        self.actionPaletteBackground.setCheckable(False)
        self.actionPaletteBackground.setObjectName("actionPaletteBackground")
        self.actionPaletteBackground.setShortcut("CTRL+P")
        self.actionPaletteBackground.setText("Palette de couleurs arrière plan")

        self.actionPaletteText = QtWidgets.QAction ( Tester )
        self.actionPaletteText.setCheckable(False)
        self.actionPaletteText.setObjectName("actionPaletteText")
        self.actionPaletteText.setShortcut("CTRL+Q")
        self.actionPaletteText.setText("Palette de couleurs texte")

        self.actionMode_clair.setShortcut("CTRL+C")

        self.actionMode_sombre.setShortcut("CTRL+S")

        abspath = os.path.dirname(__file__)
        iconFR = os.path.join(abspath,'images/drapeauFrance.png')
        self.actionFR.setIcon(QtGui.QIcon(iconFR))
        self.actionFR.setShortcut("CTRL+F")

        abspath = os.path.dirname(__file__)
        iconENG = os.path.join(abspath,'images/drapeauGB.jpg')
        self.actionENG.setIcon(QtGui.QIcon(iconENG))
        self.actionENG.setShortcut("CTRL+E")

        self.menuCouleur.addAction(self.actionMode_clair)
        self.menuCouleur.addAction(self.actionMode_sombre)

        self.menuFont = QtWidgets.QMenu ( self.menuAffichage )
        self.menuFont.setObjectName("menuFont")
        self.menuAffichage.addMenu(self.menuFont)
        self.menuFont.addAction(self.actionStyle)
        self.menuFont.addAction(self.actionStyleDefault)
        self.menuFont.setTitle("Modifier le style")

        self.menuCouleur.addAction(self.actionPaletteBackground)
        self.menuCouleur.addAction(self.actionPaletteText)

        self.menuAffichage.addAction(self.menuCouleur.menuAction())
        self.menuAffichage.addSeparator()
        self.menuAffichage.addAction(self.menuLanguage_2.menuAction())
        self.menuBar.addAction(self.menuAffichage.menuAction())
        self.menuBar.addAction(self.menuAide.menuAction())

        self.graphic = MplCanvas(self, width=5, height=4, dpi=100)
        self.gridLayout_5.addWidget(self.graphic, 0, 0, 1, 1)
        self.gridLayout_9.addLayout(self.gridLayout_5, 0, 0, 1, 1)

        # self.retranslateUi2(Tester)
        self.tabWidget.setCurrentIndex(3)
        QtCore.QMetaObject.connectSlotsByName(Tester)

        self.actionMode_clair.triggered.connect(self.modeClair)
        self.actionMode_sombre.triggered.connect(self.modeSombre)

        self.actionStyle.triggered.connect(self.dialogStyle)
        self.actionStyleDefault.triggered.connect(self.styleDefault)
        self.action_propos.triggered.connect(self.indexPropos)
        self.actionRepo.triggered.connect(self.openRepo)
        self.DisplayPlotButton.clicked.connect(self.PlotData)
        self.actionPaletteBackground.triggered.connect(self.choixCouleurBackground)
        self.actionPaletteText.triggered.connect(self.choixCouleurText)

        self.actionENG.triggered.connect(self.ENG)
        self.actionFR.triggered.connect(self.FR)

        abspath = os.path.dirname(__file__)
        langDefault = os.path.join(abspath,'lang/Default.cfg')
        self.configLangDefault = configFile.configFile ( configFilename=langDefault , encoding = "utf-8")
        self.paramLangDefault = self.configLangDefault.configuration ().get ( 'langDefault', 'lastChosen' )
        getattr(self, self.paramLangDefault)()
        # eval ( 'self.' + self.paramLangDefault + '()' )

    def FR(self):
        self.configLangDefault.changeConfig('langDefault', 'lastChosen', 'FR')
        abspath = os.path.dirname(__file__)
        langFR = os.path.join(abspath,'lang/FR.cfg')
        self.configLang = configFile.configFile(configFilename=langFR, encoding = "utf-8")
        self.retranslateUi2()

    def ENG(self):
        self.configLangDefault.changeConfig('langDefault', 'lastChosen', 'ENG')
        abspath = os.path.dirname(__file__)
        langENG = os.path.join(abspath,'lang/ENG.cfg')
        self.configLang = configFile.configFile(configFilename=langENG, encoding = "utf-8")
        self.retranslateUi2()


    def retranslateUi2(self):
        _translate = QtCore.QCoreApplication.translate

        #Buttons
        self.ToConnectButton.setText(_translate("Tester", self.configLang.configuration().get('buttons', 'ToConnectButton')))
        self.ToDisconnectButton.setText(_translate("Tester", self.configLang.configuration().get('buttons', 'ToDisconnectButton')))
        self.ToResetDistance.setText(_translate("Tester", self.configLang.configuration().get('buttons', 'ToResetDistance')))
        self.DirectoryConfirmB.setText(_translate("Tester", self.configLang.configuration().get('buttons', 'DirectoryConfirmB')))
        self.FileConfirmButton.setText(_translate("Tester", self.configLang.configuration().get('buttons', 'FileConfirmButton')))
        self.DataIntervalButton.setText(_translate("Tester", self.configLang.configuration().get('buttons', 'DataIntervalButton')))
        self.DisplayPlotButton.setText(_translate("Tester", self.configLang.configuration().get('buttons', 'DisplayPlotButton')))
        self.CloseButton.setText(_translate("Tester", self.configLang.configuration().get('buttons', 'CloseButton')))

        #Text labels
        self.labelRemerciements.setText(_translate("Tester", self.configLang.configuration().get('textLabels', 'labelRemerciements')))
        self.lcdTextDistance.setText(_translate("Tester", self.configLang.configuration().get('textLabels', 'lcdTextDistance')))
        self.lcdTextPositionChange.setText(_translate("Tester", self.configLang.configuration().get('textLabels', 'lcdTextPositionChange')))
        self.lcdTextTimeChange.setText(_translate("Tester", self.configLang.configuration().get('textLabels', 'lcdTextTimeChange')))
        self.lcdTextTimeRecording.setText(_translate("Tester", self.configLang.configuration().get('textLabels', 'lcdTextTimeRecording')))
        self.urlRepo_2.setText(_translate("Tester", self.configLang.configuration().get('textLabels', 'urlRepo_2')))
        try:
            repoAdress=self.config.configuration().get('REPO','GitHub')
        except:
            repoAdress='https://github.com/WilliamBonilla62/GUIPythonEncodeur/'
        hrefRepoAdress=f'<a href="{repoAdress}">{repoAdress}</a>'
        self.urlRepo.setText(_translate("Tester",hrefRepoAdress))
        # self.urlRepo.setText(_translate("Tester", self.configLang.configuration().get('textLabels', 'urlRepo')))

        #Group boxes
        self.groupBox_3.setTitle(_translate("Tester", self.configLang.configuration().get('groupBoxes', 'groupBox_3')))
        self.groupBox_5.setTitle(_translate("Tester", self.configLang.configuration().get('groupBoxes', 'groupBox_5')))
        self.groupBox_2.setTitle(_translate("Tester", self.configLang.configuration().get('groupBoxes', 'groupBox_2')))
        self.RegisterEnco.setText(_translate("Tester", self.configLang.configuration().get('groupBoxes', 'RegisterEnco')))

        #tabs
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate("Tester", self.configLang.configuration().get('tabs', 'tab')))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), _translate("Tester", self.configLang.configuration().get('tabs', 'tab_2')))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_3), _translate("Tester", self.configLang.configuration().get('tabs', 'tab_3')))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_4), _translate("Tester", self.configLang.configuration().get('tabs', 'tab_4')))

        #Text boxes
        self.textBoxDirectory.setText(_translate("Tester", self.configLang.configuration().get('textBoxes', 'textBoxDirectory')))
        self.textBoxFile.setText(_translate("Tester", self.configLang.configuration().get('textBoxes', 'textBoxFile')))
        self.textBoxDataInterval.setText(_translate("Tester", self.configLang.configuration().get('textBoxes', 'textBoxDataInterval')))

        #Menus
        self.menuAffichage.setTitle(_translate("Tester", self.configLang.configuration().get('menus', 'menuAffichage')))
        self.menuCouleur.setTitle(_translate("Tester", self.configLang.configuration().get('menus', 'menuCouleur')))
        self.menuAide.setTitle(_translate("Tester", self.configLang.configuration().get('menus', 'menuAide')))
        self.menuFont.setTitle(_translate("Tester", self.configLang.configuration().get('menus', 'menuFont')))

        #Actions
        self.actionStyle.setText(_translate("Tester", self.configLang.configuration().get('actions', 'actionStyle')))
        self.actionStyleDefault.setText(_translate("Tester", self.configLang.configuration().get('actions', 'actionStyleDefault')))
        self.actionPaletteBackground.setText(_translate("Tester", self.configLang.configuration().get('actions', 'actionPaletteBackground')))
        self.actionPaletteText.setText(_translate("Tester", self.configLang.configuration().get('actions', 'actionPaletteText')))
        self.actionMode_clair.setText(_translate("Tester", self.configLang.configuration().get('actions', 'actionMode_clair')))
        self.actionMode_sombre.setText(_translate("Tester", self.configLang.configuration().get('actions', 'actionMode_sombre')))
        self.actionFR.setText(_translate("Tester", self.configLang.configuration().get('actions', 'actionFR')))
        self.actionENG.setText(_translate("Tester", self.configLang.configuration().get('actions', 'actionENG')))
        self.actionRepo.setText(_translate("Tester", self.configLang.configuration().get('actions', 'actionRepo')))
        self.action_propos.setText(_translate("Tester", self.configLang.configuration().get('actions', 'action_propos')))




if __name__ == "__main__":

    import sys

    app = QtWidgets.QApplication(sys.argv)
    Tester = QtWidgets.QMainWindow()
    ui = Ui_Style()
    ui.setupUi(Tester)
    Tester.show()
    sys.exit(app.exec_())

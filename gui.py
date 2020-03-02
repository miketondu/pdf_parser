# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'gui1.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(320, 240)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.selectPDF = QtWidgets.QPushButton(self.centralwidget)
        self.selectPDF.setGeometry(QtCore.QRect(20, 20, 121, 41))
        self.selectPDF.setObjectName("selectPDF")
        self.selectSaveFolder = QtWidgets.QPushButton(self.centralwidget)
        self.selectSaveFolder.setGeometry(QtCore.QRect(169, 20, 121, 41))
        self.selectSaveFolder.setObjectName("selectSaveFolder")
        self.runButton = QtWidgets.QPushButton(self.centralwidget)
        self.runButton.setGeometry(QtCore.QRect(100, 130, 121, 41))
        self.runButton.setObjectName("runButton")
        self.labelPATH = QtWidgets.QLabel(self.centralwidget)
        self.labelPATH.setGeometry(QtCore.QRect(30, 80, 251, 20))
        self.labelPATH.setObjectName("labelPATH")
        self.labelPATH_2 = QtWidgets.QLabel(self.centralwidget)
        self.labelPATH_2.setGeometry(QtCore.QRect(30, 110, 181, 20))
        self.labelPATH_2.setText("")
        self.labelPATH_2.setObjectName("labelPATH_2")
        #self.checkBox = QtWidgets.QCheckBox(self.centralwidget)
        #elf.checkBox.setGeometry(QtCore.QRect(30, 110, 171, 20))
        #self.checkBox.setObjectName("checkBox")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 320, 22))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "PDF Parser"))
        self.selectPDF.setText(_translate("MainWindow", "Select PDF files"))
        self.selectSaveFolder.setText(_translate("MainWindow", "Set save PATH"))
        self.runButton.setText(_translate("MainWindow", "RUN!"))
        self.labelPATH.setText(_translate("MainWindow", "Save dir: default pdf location"))
        #self.checkBox.setText(_translate("MainWindow", "Process Only Summary"))


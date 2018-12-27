# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'form.ui',
# licensing of 'form.ui' applies.
#
# Created: Thu Dec 20 17:55:28 2018
#      by: pyside2-uic  running on PySide2 5.11.2
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(520, 438)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(Form)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.listWidget_files = QtWidgets.QListWidget(Form)
        self.listWidget_files.setObjectName("listWidget_files")
        self.horizontalLayout.addWidget(self.listWidget_files)
        self.listWidget_format = QtWidgets.QListWidget(Form)
        self.listWidget_format.setObjectName("listWidget_format")
        self.horizontalLayout.addWidget(self.listWidget_format)
        self.verticalLayout_2.addLayout(self.horizontalLayout)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.progbarTotal = QtWidgets.QProgressBar(Form)
        self.progbarTotal.setProperty("value", 24)
        self.progbarTotal.setObjectName("progbarTotal")
        self.verticalLayout.addWidget(self.progbarTotal)
        self.progbarCurrent = QtWidgets.QProgressBar(Form)
        self.progbarCurrent.setProperty("value", 24)
        self.progbarCurrent.setObjectName("progbarCurrent")
        self.verticalLayout.addWidget(self.progbarCurrent)
        self.verticalLayout_2.addLayout(self.verticalLayout)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.btnOpen = QtWidgets.QPushButton(Form)
        self.btnOpen.setText("")
        self.btnOpen.setObjectName("btnOpen")
        self.horizontalLayout_2.addWidget(self.btnOpen)
        self.btnStart = QtWidgets.QPushButton(Form)
        self.btnStart.setText("")
        self.btnStart.setObjectName("btnStart")
        self.horizontalLayout_2.addWidget(self.btnStart)
        self.btnStop = QtWidgets.QPushButton(Form)
        self.btnStop.setText("")
        self.btnStop.setObjectName("btnStop")
        self.horizontalLayout_2.addWidget(self.btnStop)
        self.pushButton = QtWidgets.QPushButton(Form)
        self.pushButton.setText("")
        self.pushButton.setObjectName("pushButton")
        self.horizontalLayout_2.addWidget(self.pushButton)
        self.verticalLayout_2.addLayout(self.horizontalLayout_2)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(QtWidgets.QApplication.translate("Form", "Form", None, -1))


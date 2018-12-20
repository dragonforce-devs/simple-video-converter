# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '.\form.ui',
# licensing of '.\form.ui' applies.
#
# Created: Thu Dec 20 00:49:52 2018
#      by: pyside2-uic  running on PySide2 5.12.0
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(520, 438)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(Form)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.layoutViews = QtWidgets.QHBoxLayout()
        self.layoutViews.setObjectName("layoutViews")
        self.listViewFiles = QtWidgets.QListView(Form)
        self.listViewFiles.setObjectName("listViewFiles")
        self.layoutViews.addWidget(self.listViewFiles)
        self.listViewTypes = QtWidgets.QListView(Form)
        self.listViewTypes.setObjectName("listViewTypes")
        self.layoutViews.addWidget(self.listViewTypes)
        self.verticalLayout_2.addLayout(self.layoutViews)
        self.layoutProgressBars = QtWidgets.QVBoxLayout()
        self.layoutProgressBars.setObjectName("layoutProgressBars")
        self.progressBarCurrent = QtWidgets.QProgressBar(Form)
        self.progressBarCurrent.setProperty("value", 24)
        self.progressBarCurrent.setObjectName("progressBarCurrent")
        self.layoutProgressBars.addWidget(self.progressBarCurrent)
        self.progressBarTotal = QtWidgets.QProgressBar(Form)
        self.progressBarTotal.setProperty("value", 24)
        self.progressBarTotal.setObjectName("progressBarTotal")
        self.layoutProgressBars.addWidget(self.progressBarTotal)
        self.verticalLayout_2.addLayout(self.layoutProgressBars)
        self.layoutButtons = QtWidgets.QHBoxLayout()
        self.layoutButtons.setObjectName("layoutButtons")
        self.btnAdd = QtWidgets.QPushButton(Form)
        self.btnAdd.setObjectName("btnAdd")
        self.layoutButtons.addWidget(self.btnAdd)
        self.btnConvert = QtWidgets.QPushButton(Form)
        self.btnConvert.setObjectName("btnConvert")
        self.layoutButtons.addWidget(self.btnConvert)
        self.btnStop = QtWidgets.QPushButton(Form)
        self.btnStop.setObjectName("btnStop")
        self.layoutButtons.addWidget(self.btnStop)
        self.verticalLayout_2.addLayout(self.layoutButtons)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(QtWidgets.QApplication.translate("Form", "Form", None, -1))
        self.btnAdd.setText(QtWidgets.QApplication.translate("Form", "Add Files", None, -1))
        self.btnConvert.setText(QtWidgets.QApplication.translate("Form", "Convert", None, -1))
        self.btnStop.setText(QtWidgets.QApplication.translate("Form", "Stop", None, -1))


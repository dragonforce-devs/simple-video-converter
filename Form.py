# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'form.ui',
# licensing of 'form.ui' applies.
#
# Created: Tue Jan  1 10:53:35 2019
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
        self.tabWidget = QtWidgets.QTabWidget(Form)
        self.tabWidget.setObjectName("tabWidget")
        self.tab = QtWidgets.QWidget()
        self.tab.setObjectName("tab")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.tab)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.listViewFiles = QtWidgets.QListView(self.tab)
        self.listViewFiles.setObjectName("listViewFiles")
        self.horizontalLayout_3.addWidget(self.listViewFiles)
        self.listViewFormat = QtWidgets.QListView(self.tab)
        self.listViewFormat.setObjectName("listViewFormat")
        self.horizontalLayout_3.addWidget(self.listViewFormat)
        self.verticalLayout_4.addLayout(self.horizontalLayout_3)
        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.progbarTotal = QtWidgets.QProgressBar(self.tab)
        self.progbarTotal.setProperty("value", 24)
        self.progbarTotal.setObjectName("progbarTotal")
        self.verticalLayout.addWidget(self.progbarTotal)
        self.progbarCurrent = QtWidgets.QProgressBar(self.tab)
        self.progbarCurrent.setProperty("value", 24)
        self.progbarCurrent.setObjectName("progbarCurrent")
        self.verticalLayout.addWidget(self.progbarCurrent)
        self.verticalLayout_3.addLayout(self.verticalLayout)
        self.verticalLayout_4.addLayout(self.verticalLayout_3)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.btnOpen = QtWidgets.QPushButton(self.tab)
        self.btnOpen.setText("")
        self.btnOpen.setObjectName("btnOpen")
        self.horizontalLayout.addWidget(self.btnOpen)
        self.btnStart = QtWidgets.QPushButton(self.tab)
        self.btnStart.setText("")
        self.btnStart.setObjectName("btnStart")
        self.horizontalLayout.addWidget(self.btnStart)
        self.btnStop = QtWidgets.QPushButton(self.tab)
        self.btnStop.setText("")
        self.btnStop.setObjectName("btnStop")
        self.horizontalLayout.addWidget(self.btnStop)
        self.btnClearQueue = QtWidgets.QPushButton(self.tab)
        self.btnClearQueue.setObjectName("btnClearQueue")
        self.horizontalLayout.addWidget(self.btnClearQueue)
        self.verticalLayout_4.addLayout(self.horizontalLayout)
        self.tabWidget.addTab(self.tab, "")
        self.tab_2 = QtWidgets.QWidget()
        self.tab_2.setObjectName("tab_2")
        self.tabWidget.addTab(self.tab_2, "")
        self.verticalLayout_2.addWidget(self.tabWidget)

        self.retranslateUi(Form)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(QtWidgets.QApplication.translate("Form", "Form", None, -1))
        self.btnClearQueue.setText(QtWidgets.QApplication.translate("Form", "Clear Queue", None, -1))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), QtWidgets.QApplication.translate("Form", "Main", None, -1))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), QtWidgets.QApplication.translate("Form", "Additional Settings", None, -1))


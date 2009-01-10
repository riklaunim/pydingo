# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'dingo.ui'
#
# Created: Sat Jan 10 19:35:48 2009
#      by: PyQt4 UI code generator 4.4.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_Dingo(object):
    def setupUi(self, Dingo):
        Dingo.setObjectName("Dingo")
        Dingo.resize(573, 549)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/ui/pydingo.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        Dingo.setWindowIcon(icon)
        self.centralwidget = QtGui.QWidget(Dingo)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtGui.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.splitter = QtGui.QSplitter(self.centralwidget)
        self.splitter.setOrientation(QtCore.Qt.Vertical)
        self.splitter.setObjectName("splitter")
        self.mainFrame = QtGui.QFrame(self.splitter)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.mainFrame.sizePolicy().hasHeightForWidth())
        self.mainFrame.setSizePolicy(sizePolicy)
        self.mainFrame.setFrameShape(QtGui.QFrame.NoFrame)
        self.mainFrame.setFrameShadow(QtGui.QFrame.Plain)
        self.mainFrame.setLineWidth(1)
        self.mainFrame.setMidLineWidth(0)
        self.mainFrame.setObjectName("mainFrame")
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.mainFrame)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.dockFrame = QtGui.QFrame(self.splitter)
        self.dockFrame.setFrameShape(QtGui.QFrame.NoFrame)
        self.dockFrame.setFrameShadow(QtGui.QFrame.Raised)
        self.dockFrame.setObjectName("dockFrame")
        self.verticalLayout.addWidget(self.splitter)
        Dingo.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(Dingo)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 573, 23))
        self.menubar.setObjectName("menubar")
        Dingo.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(Dingo)
        self.statusbar.setObjectName("statusbar")
        Dingo.setStatusBar(self.statusbar)

        self.retranslateUi(Dingo)
        QtCore.QMetaObject.connectSlotsByName(Dingo)

    def retranslateUi(self, Dingo):
        Dingo.setWindowTitle(QtGui.QApplication.translate("Dingo", "Dingo", None, QtGui.QApplication.UnicodeUTF8))

import resources_rc

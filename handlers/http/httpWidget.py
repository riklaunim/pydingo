# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'httpWidget.ui'
#
# Created: Mon Dec  1 23:26:03 2008
#      by: PyQt4 UI code generator 4.4.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_HttpWidget(object):
    def setupUi(self, HttpWidget):
        HttpWidget.setObjectName("HttpWidget")
        HttpWidget.resize(700, 426)
        self.gridLayout = QtGui.QGridLayout(HttpWidget)
        self.gridLayout.setObjectName("gridLayout")
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.newTab = QtGui.QPushButton(HttpWidget)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("media/file/new_tab.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.newTab.setIcon(icon)
        self.newTab.setIconSize(QtCore.QSize(32, 32))
        self.newTab.setObjectName("newTab")
        self.horizontalLayout.addWidget(self.newTab)
        self.back = QtGui.QPushButton(HttpWidget)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap("media/file/back.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.back.setIcon(icon1)
        self.back.setIconSize(QtCore.QSize(32, 32))
        self.back.setObjectName("back")
        self.horizontalLayout.addWidget(self.back)
        self.next = QtGui.QPushButton(HttpWidget)
        self.next.setEnabled(False)
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap("media/file/next.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.next.setIcon(icon2)
        self.next.setIconSize(QtCore.QSize(32, 32))
        self.next.setObjectName("next")
        self.horizontalLayout.addWidget(self.next)
        self.up = QtGui.QPushButton(HttpWidget)
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap("media/file/up.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.up.setIcon(icon3)
        self.up.setIconSize(QtCore.QSize(32, 32))
        self.up.setObjectName("up")
        self.horizontalLayout.addWidget(self.up)
        self.home = QtGui.QPushButton(HttpWidget)
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap("media/file/home.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.home.setIcon(icon4)
        self.home.setIconSize(QtCore.QSize(32, 32))
        self.home.setObjectName("home")
        self.horizontalLayout.addWidget(self.home)
        self.url = QtGui.QLineEdit(HttpWidget)
        self.url.setObjectName("url")
        self.horizontalLayout.addWidget(self.url)
        self.detach = QtGui.QPushButton(HttpWidget)
        icon5 = QtGui.QIcon()
        icon5.addPixmap(QtGui.QPixmap("media/file/detach.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.detach.setIcon(icon5)
        self.detach.setIconSize(QtCore.QSize(32, 32))
        self.detach.setObjectName("detach")
        self.horizontalLayout.addWidget(self.detach)
        self.close = QtGui.QPushButton(HttpWidget)
        icon6 = QtGui.QIcon()
        icon6.addPixmap(QtGui.QPixmap("media/file/close.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.close.setIcon(icon6)
        self.close.setIconSize(QtCore.QSize(32, 32))
        self.close.setObjectName("close")
        self.horizontalLayout.addWidget(self.close)
        self.gridLayout.addLayout(self.horizontalLayout, 0, 0, 1, 1)
        self.webView = QtWebKit.QWebView(HttpWidget)
        self.webView.setUrl(QtCore.QUrl("about:blank"))
        self.webView.setObjectName("webView")
        self.gridLayout.addWidget(self.webView, 1, 0, 1, 1)

        self.retranslateUi(HttpWidget)
        QtCore.QMetaObject.connectSlotsByName(HttpWidget)

    def retranslateUi(self, HttpWidget):
        HttpWidget.setWindowTitle(QtGui.QApplication.translate("HttpWidget", "Form", None, QtGui.QApplication.UnicodeUTF8))
        self.newTab.setToolTip(QtGui.QApplication.translate("HttpWidget", "New Tab", None, QtGui.QApplication.UnicodeUTF8))
        self.back.setToolTip(QtGui.QApplication.translate("HttpWidget", "Back", None, QtGui.QApplication.UnicodeUTF8))
        self.next.setToolTip(QtGui.QApplication.translate("HttpWidget", "Next", None, QtGui.QApplication.UnicodeUTF8))
        self.up.setToolTip(QtGui.QApplication.translate("HttpWidget", "Up", None, QtGui.QApplication.UnicodeUTF8))
        self.home.setToolTip(QtGui.QApplication.translate("HttpWidget", "Home", None, QtGui.QApplication.UnicodeUTF8))
        self.detach.setToolTip(QtGui.QApplication.translate("HttpWidget", "Detach", None, QtGui.QApplication.UnicodeUTF8))
        self.close.setToolTip(QtGui.QApplication.translate("HttpWidget", "Close", None, QtGui.QApplication.UnicodeUTF8))

from PyQt4 import QtWebKit

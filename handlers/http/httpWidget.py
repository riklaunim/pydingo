# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'httpWidget.ui'
#
# Created: Mon Feb 16 01:02:47 2009
#      by: PyQt4 UI code generator 4.4.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_HttpWidget(object):
    def setupUi(self, HttpWidget):
        HttpWidget.setObjectName("HttpWidget")
        HttpWidget.resize(700, 426)
        self.verticalLayout = QtGui.QVBoxLayout(HttpWidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.newTab = QtGui.QPushButton(HttpWidget)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/ui/media/file/new_tab.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.newTab.setIcon(icon)
        self.newTab.setIconSize(QtCore.QSize(24, 24))
        self.newTab.setObjectName("newTab")
        self.horizontalLayout.addWidget(self.newTab)
        self.back = QtGui.QPushButton(HttpWidget)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/ui/media/file/back.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.back.setIcon(icon1)
        self.back.setIconSize(QtCore.QSize(24, 24))
        self.back.setObjectName("back")
        self.horizontalLayout.addWidget(self.back)
        self.next = QtGui.QPushButton(HttpWidget)
        self.next.setEnabled(False)
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(":/ui/media/file/next.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.next.setIcon(icon2)
        self.next.setIconSize(QtCore.QSize(24, 24))
        self.next.setObjectName("next")
        self.horizontalLayout.addWidget(self.next)
        self.stop = QtGui.QPushButton(HttpWidget)
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(":/ui/media/file/stop.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.stop.setIcon(icon3)
        self.stop.setIconSize(QtCore.QSize(24, 24))
        self.stop.setObjectName("stop")
        self.horizontalLayout.addWidget(self.stop)
        self.reload = QtGui.QPushButton(HttpWidget)
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap(":/ui/media/file/reload.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.reload.setIcon(icon4)
        self.reload.setIconSize(QtCore.QSize(24, 24))
        self.reload.setObjectName("reload")
        self.horizontalLayout.addWidget(self.reload)
        self.up = QtGui.QPushButton(HttpWidget)
        icon5 = QtGui.QIcon()
        icon5.addPixmap(QtGui.QPixmap(":/ui/media/file/up.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.up.setIcon(icon5)
        self.up.setIconSize(QtCore.QSize(24, 24))
        self.up.setObjectName("up")
        self.horizontalLayout.addWidget(self.up)
        self.home = QtGui.QPushButton(HttpWidget)
        icon6 = QtGui.QIcon()
        icon6.addPixmap(QtGui.QPixmap(":/ui/media/file/home.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.home.setIcon(icon6)
        self.home.setIconSize(QtCore.QSize(24, 24))
        self.home.setObjectName("home")
        self.horizontalLayout.addWidget(self.home)
        self.url = QtGui.QLineEdit(HttpWidget)
        self.url.setObjectName("url")
        self.horizontalLayout.addWidget(self.url)
        self.detach = QtGui.QPushButton(HttpWidget)
        icon7 = QtGui.QIcon()
        icon7.addPixmap(QtGui.QPixmap(":/ui/media/file/detach.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.detach.setIcon(icon7)
        self.detach.setIconSize(QtCore.QSize(24, 24))
        self.detach.setObjectName("detach")
        self.horizontalLayout.addWidget(self.detach)
        self.close = QtGui.QPushButton(HttpWidget)
        icon8 = QtGui.QIcon()
        icon8.addPixmap(QtGui.QPixmap(":/ui/media/file/close.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.close.setIcon(icon8)
        self.close.setIconSize(QtCore.QSize(24, 24))
        self.close.setObjectName("close")
        self.horizontalLayout.addWidget(self.close)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.webView = QtWebKit.QWebView(HttpWidget)
        self.webView.setUrl(QtCore.QUrl("about:blank"))
        self.webView.setObjectName("webView")
        self.verticalLayout.addWidget(self.webView)

        self.retranslateUi(HttpWidget)
        QtCore.QMetaObject.connectSlotsByName(HttpWidget)

    def retranslateUi(self, HttpWidget):
        HttpWidget.setWindowTitle(QtGui.QApplication.translate("HttpWidget", "Form", None, QtGui.QApplication.UnicodeUTF8))
        self.newTab.setToolTip(QtGui.QApplication.translate("HttpWidget", "New Tab", None, QtGui.QApplication.UnicodeUTF8))
        self.back.setToolTip(QtGui.QApplication.translate("HttpWidget", "Back", None, QtGui.QApplication.UnicodeUTF8))
        self.next.setToolTip(QtGui.QApplication.translate("HttpWidget", "Next", None, QtGui.QApplication.UnicodeUTF8))
        self.stop.setToolTip(QtGui.QApplication.translate("HttpWidget", "Stop", None, QtGui.QApplication.UnicodeUTF8))
        self.reload.setToolTip(QtGui.QApplication.translate("HttpWidget", "Reload", None, QtGui.QApplication.UnicodeUTF8))
        self.up.setToolTip(QtGui.QApplication.translate("HttpWidget", "Up", None, QtGui.QApplication.UnicodeUTF8))
        self.home.setToolTip(QtGui.QApplication.translate("HttpWidget", "Home", None, QtGui.QApplication.UnicodeUTF8))
        self.detach.setToolTip(QtGui.QApplication.translate("HttpWidget", "Detach", None, QtGui.QApplication.UnicodeUTF8))
        self.close.setToolTip(QtGui.QApplication.translate("HttpWidget", "Close", None, QtGui.QApplication.UnicodeUTF8))

from PyQt4 import QtWebKit
import resources_rc

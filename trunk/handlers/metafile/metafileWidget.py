# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'metafileWidget.ui'
#
# Created: Mon Dec  1 16:14:20 2008
#      by: PyQt4 UI code generator 4.4.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_MetafileWidget(object):
    def setupUi(self, MetafileWidget):
        MetafileWidget.setObjectName("MetafileWidget")
        MetafileWidget.resize(745, 426)
        self.verticalLayout = QtGui.QVBoxLayout(MetafileWidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.newTab = QtGui.QPushButton(MetafileWidget)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("media/file/new_tab.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.newTab.setIcon(icon)
        self.newTab.setIconSize(QtCore.QSize(32, 32))
        self.newTab.setObjectName("newTab")
        self.horizontalLayout.addWidget(self.newTab)
        self.back = QtGui.QPushButton(MetafileWidget)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap("media/file/back.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.back.setIcon(icon1)
        self.back.setIconSize(QtCore.QSize(32, 32))
        self.back.setObjectName("back")
        self.horizontalLayout.addWidget(self.back)
        self.next = QtGui.QPushButton(MetafileWidget)
        self.next.setEnabled(False)
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap("media/file/next.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.next.setIcon(icon2)
        self.next.setIconSize(QtCore.QSize(32, 32))
        self.next.setObjectName("next")
        self.horizontalLayout.addWidget(self.next)
        self.up = QtGui.QPushButton(MetafileWidget)
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap("media/file/up.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.up.setIcon(icon3)
        self.up.setIconSize(QtCore.QSize(32, 32))
        self.up.setObjectName("up")
        self.horizontalLayout.addWidget(self.up)
        self.home = QtGui.QPushButton(MetafileWidget)
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap("media/file/home.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.home.setIcon(icon4)
        self.home.setIconSize(QtCore.QSize(32, 32))
        self.home.setObjectName("home")
        self.horizontalLayout.addWidget(self.home)
        self.url = QtGui.QLineEdit(MetafileWidget)
        self.url.setObjectName("url")
        self.horizontalLayout.addWidget(self.url)
        self.editThis = QtGui.QPushButton(MetafileWidget)
        self.editThis.setEnabled(False)
        icon5 = QtGui.QIcon()
        icon5.addPixmap(QtGui.QPixmap("media/file/edit.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.editThis.setIcon(icon5)
        self.editThis.setIconSize(QtCore.QSize(32, 32))
        self.editThis.setCheckable(False)
        self.editThis.setObjectName("editThis")
        self.horizontalLayout.addWidget(self.editThis)
        self.detach = QtGui.QPushButton(MetafileWidget)
        icon6 = QtGui.QIcon()
        icon6.addPixmap(QtGui.QPixmap("media/file/detach.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.detach.setIcon(icon6)
        self.detach.setIconSize(QtCore.QSize(32, 32))
        self.detach.setObjectName("detach")
        self.horizontalLayout.addWidget(self.detach)
        self.close = QtGui.QPushButton(MetafileWidget)
        icon7 = QtGui.QIcon()
        icon7.addPixmap(QtGui.QPixmap("media/file/close.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.close.setIcon(icon7)
        self.close.setIconSize(QtCore.QSize(32, 32))
        self.close.setObjectName("close")
        self.horizontalLayout.addWidget(self.close)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.splitter = QtGui.QSplitter(MetafileWidget)
        self.splitter.setOrientation(QtCore.Qt.Horizontal)
        self.splitter.setObjectName("splitter")
        self.groupBox = QtGui.QGroupBox(self.splitter)
        self.groupBox.setObjectName("groupBox")
        self.toolBox = QtGui.QToolBox(self.splitter)
        self.toolBox.setObjectName("toolBox")
        self.strona = QtGui.QWidget()
        self.strona.setObjectName("strona")
        self.toolBox.addItem(self.strona, "")
        self.page = QtGui.QWidget()
        self.page.setGeometry(QtCore.QRect(0, 0, 237, 112))
        self.page.setObjectName("page")
        self.toolBox.addItem(self.page, "")
        self.page_2 = QtGui.QWidget()
        self.page_2.setGeometry(QtCore.QRect(0, 0, 237, 112))
        self.page_2.setObjectName("page_2")
        self.toolBox.addItem(self.page_2, "")
        self.verticalLayout.addWidget(self.splitter)

        self.retranslateUi(MetafileWidget)
        self.toolBox.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MetafileWidget)

    def retranslateUi(self, MetafileWidget):
        MetafileWidget.setWindowTitle(QtGui.QApplication.translate("MetafileWidget", "Form", None, QtGui.QApplication.UnicodeUTF8))
        self.newTab.setToolTip(QtGui.QApplication.translate("MetafileWidget", "New Tab", None, QtGui.QApplication.UnicodeUTF8))
        self.back.setToolTip(QtGui.QApplication.translate("MetafileWidget", "Back", None, QtGui.QApplication.UnicodeUTF8))
        self.next.setToolTip(QtGui.QApplication.translate("MetafileWidget", "Next", None, QtGui.QApplication.UnicodeUTF8))
        self.up.setToolTip(QtGui.QApplication.translate("MetafileWidget", "Up", None, QtGui.QApplication.UnicodeUTF8))
        self.home.setToolTip(QtGui.QApplication.translate("MetafileWidget", "Home", None, QtGui.QApplication.UnicodeUTF8))
        self.editThis.setToolTip(QtGui.QApplication.translate("MetafileWidget", "Detach", None, QtGui.QApplication.UnicodeUTF8))
        self.detach.setToolTip(QtGui.QApplication.translate("MetafileWidget", "Detach", None, QtGui.QApplication.UnicodeUTF8))
        self.close.setToolTip(QtGui.QApplication.translate("MetafileWidget", "Close", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox.setTitle(QtGui.QApplication.translate("MetafileWidget", "Actions", None, QtGui.QApplication.UnicodeUTF8))
        self.toolBox.setItemText(self.toolBox.indexOf(self.strona), QtGui.QApplication.translate("MetafileWidget", "File Info", None, QtGui.QApplication.UnicodeUTF8))
        self.toolBox.setItemText(self.toolBox.indexOf(self.page), QtGui.QApplication.translate("MetafileWidget", "KDE", None, QtGui.QApplication.UnicodeUTF8))
        self.toolBox.setItemText(self.toolBox.indexOf(self.page_2), QtGui.QApplication.translate("MetafileWidget", "GNOME", None, QtGui.QApplication.UnicodeUTF8))


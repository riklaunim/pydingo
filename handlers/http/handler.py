# -*- coding: utf-8 -*-

from PyQt4 import QtCore, QtGui
from httpWidget import Ui_HttpWidget

class webWidget(QtGui.QWidget):
	def __init__(self, parent=None, url=False, mainWindow=False, newTab=False):
		super(webWidget, self).__init__(parent)
		self.ui = Ui_HttpWidget()
		self.ui.setupUi(self)
		self.parent = parent
		self.mainWindow = mainWindow
		# set the lineEdit-URL to be as high as buttons
		self.ui.url.setSizePolicy(QtGui.QSizePolicy.MinimumExpanding,QtGui.QSizePolicy.Preferred)
		
		# set the url
		if not url:
			url = self.ui.url.text()

		self.ui.url.setText(url)
		self.mainWindow.update_back_bucket(unicode(url))
		
		# name the tab as current folder name
		tabName = url
		
		# load page
		self.ui.webView.setUrl(QtCore.QUrl(url))
		
		if newTab:
			index = parent.addTab(self, tabName)
			parent.setCurrentIndex(index)
		else:
			index = parent.currentIndex()
			parent.removeTab(index)
			parent.insertTab(index, self, tabName)
			parent.setCurrentIndex(index)
		
		QtCore.QObject.connect(self.ui.newTab,QtCore.SIGNAL("clicked()"), self.mainWindow.new_tab)
		QtCore.QObject.connect(self.ui.back,QtCore.SIGNAL("clicked()"), self.mainWindow.back)
		QtCore.QObject.connect(self.ui.close,QtCore.SIGNAL("clicked()"), self.mainWindow.close_tab)
		QtCore.QObject.connect(self.ui.up,QtCore.SIGNAL("clicked()"), self.mainWindow.up_clicked)
		QtCore.QObject.connect(self.ui.home,QtCore.SIGNAL("clicked()"), self.mainWindow.home_clicked)
		QtCore.QObject.connect(self.ui.url,QtCore.SIGNAL("returnPressed()"), self.mainWindow.url_handler)
		
		QtCore.QMetaObject.connectSlotsByName(self)
	
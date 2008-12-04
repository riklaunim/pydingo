# -*- coding: utf-8 -*-
from os.path import isfile, isdir, join


from PyQt4 import QtCore, QtGui
from directoryWidget import Ui_DirectoryWidget

class directoryWidget(QtGui.QWidget):
	def __init__(self, parent=None, url=False, mainWindow=False, newTab=False):
		super(directoryWidget, self).__init__(parent)
		self.ui = Ui_DirectoryWidget()
		self.ui.setupUi(self)
		self.parent = parent
		self.mainWindow = mainWindow
		# set the lineEdit-URL to be as high as buttons
		self.ui.url.setSizePolicy(QtGui.QSizePolicy.MinimumExpanding,QtGui.QSizePolicy.Preferred)
		
		# set the url
		if not url:
			url = self.ui.url.text()
		
		if url and len(url) > 0:
			pass
		else:
			url = QtCore.QDir.homePath()
		
		qdir = QtCore.QDir(url)
		self.ui.url.setText(url)
		self.mainWindow.update_back_bucket(unicode(url))
		
		# name the tab as current folder name
		tabName = qdir.dirName()
		if not tabName:
			tabName = '/'
		# set the item list
		self.ui.items.setViewMode(QtGui.QListView.IconMode)
		self.ui.items.setLayoutMode(QtGui.QListView.SinglePass)
		self.ui.items.setResizeMode(QtGui.QListView.Adjust)
		self.ui.items.setGridSize(QtCore.QSize(70, 70))
		self.ui.items.setWordWrap(True)
		self.ui.items.setWrapping(True)
		
		#self.ui.items.setMouseTracking(True)
		
		
		qdir.setFilter(QtCore.QDir.AllEntries | QtCore.QDir.NoDotAndDotDot)
		qdir.setSorting(QtCore.QDir.DirsFirst)
		qdirs = qdir.entryList()
		for d in qdirs:
			itm = QtGui.QListWidgetItem(d)
			if isdir(url+u'/'+d):
				itm.setIcon(QtGui.QIcon('media/icons/folder.png'))
			else:
				itm.setIcon(QtGui.QIcon('media/icons/file.png'))
			self.ui.items.addItem(itm)
		
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
		
		QtCore.QObject.connect(self.ui.items,QtCore.SIGNAL("itemClicked (QListWidgetItem *)"), self.item_clicked)
		QtCore.QMetaObject.connectSlotsByName(self)
	
	def keyPressEvent(self, event):
		print 'dupa'
	
	def mousePressEvent(self, event):
		print 'test'
	
	def item_clicked(self, item):
		"""
		File or folder clicked
		"""
		
		url = join(unicode(self.ui.url.text()),unicode(item.text()))
		if isdir(url) or isfile(url):
			#self.ui.url.setText(url)
			self.mainWindow.url_handler(url=url)
		else:
			print u'NOT A FILE OR DIRECTORY %s' % unicode(url)
	
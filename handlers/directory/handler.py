# -*- coding: utf-8 -*-
from os.path import isfile, isdir, join


from PyQt4 import QtCore, QtGui
from directoryWidget import Ui_DirectoryWidget

class FileManagerWidget(QtGui.QListWidget):
	def __init__(self, parent=None,):
		"""
		QListWidget with handling of mouse events - left and right clicks
		"""
		super(FileManagerWidget, self).__init__(parent)
		
		# configure the items list
		self.setViewMode(QtGui.QListView.IconMode)
		self.setLayoutMode(QtGui.QListView.SinglePass)
		self.setResizeMode(QtGui.QListView.Adjust)
		self.setGridSize(QtCore.QSize(70, 70))
		self.setWordWrap(True)
		self.setWrapping(True)
		
		self.parent = parent
		
		QtCore.QMetaObject.connectSlotsByName(self)
	
	def mouseReleaseEvent(self, event):
		"""
		Handle the event.
		for left click-release - go to the file/directory
		"""
		button = event.button()
		item = self.itemAt(event.x(), event.y())
		if item:
			self.setCurrentItem(item)
			if button == 1:
				self.item_clicked()
	
	def mousePressEvent(self, event):
		"""
		Handle the event.
		* for left clicks - ability to drag item
		* for right clicks - show context menu
		"""
		button = event.button()
		item = self.itemAt(event.x(), event.y())
		if item:
			self.setCurrentItem(item)
			if button == 1:
				print 'LEFT DRAG'
		if button == 2:
			print 'Right'
	
	def item_clicked(self):
		"""
		File or folder clicked
		"""
		item = self.currentItem().text()
		url = join(unicode(self.parent.ui.url.text()),unicode(item))
		if isdir(url) or isfile(url):
			#self.ui.url.setText(url)
			self.parent.mainWindow.url_handler(url=url)
		else:
			print u'NOT A FILE OR DIRECTORY %s' % unicode(url)


class directoryWidget(QtGui.QWidget):
	def __init__(self, parent=None, url=False, mainWindow=False, newTab=False):
		super(directoryWidget, self).__init__(parent)
		self.ui = Ui_DirectoryWidget()
		self.ui.setupUi(self)
		layout = self.layout()
		self.ui.items = FileManagerWidget(parent=self)
		layout.addWidget(self.ui.items)
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
		
		# name the tab as current folder name
		tabName = qdir.dirName()
		if not tabName:
			tabName = '/'
		
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
		QtCore.QObject.connect(self.ui.next,QtCore.SIGNAL("clicked()"), self.mainWindow.next)
		QtCore.QObject.connect(self.ui.close,QtCore.SIGNAL("clicked()"), self.mainWindow.close_tab)
		QtCore.QObject.connect(self.ui.up,QtCore.SIGNAL("clicked()"), self.mainWindow.up_clicked)
		QtCore.QObject.connect(self.ui.home,QtCore.SIGNAL("clicked()"), self.mainWindow.home_clicked)
		QtCore.QObject.connect(self.ui.url,QtCore.SIGNAL("returnPressed()"), self.mainWindow.url_handler)
		
		#QtCore.QObject.connect(self.ui.items,QtCore.SIGNAL("itemClicked (QListWidgetItem *)"), self.item_clicked)
		QtCore.QMetaObject.connectSlotsByName(self)

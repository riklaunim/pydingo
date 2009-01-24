# -*- coding: utf-8 -*-
# File manager widget based on QDirModel and QListView

from os.path import join
from os import system

from PyQt4 import QtCore, QtGui

from directoryWidget import Ui_DirectoryWidget
from view import *

from utils import gnome_meta, gio_meta
from utils import mime

class ContextMenu(QtGui.QMenu):
	"""
	Right-click context menu for a given file
	"""
	def __init__(self, parent=None, appDB=False):
		super(ContextMenu, self).__init__(parent)
		self.appDB = appDB
		self.parent = parent
		
		QtCore.QObject.connect(self,QtCore.SIGNAL("triggered(QAction *)"), self.action_triggered)
		QtCore.QMetaObject.connectSlotsByName(self)
	
	def action_triggered(self, action):
		key = unicode(action.text())
		if self.appDB.has_key(key):
			system('%s %s' % (self.appDB[key], self.appDB['URL']))
		elif key == 'Open in new tab':
			self.parent.mainWindow.url_handler(url=self.appDB['URL'], newTab=True)

class directoryWidget(QtGui.QWidget):
	def __init__(self, parent=None, url=False, mainWindow=False, newTab=False):
		super(directoryWidget, self).__init__(mainWindow.main)
		self.ui = Ui_DirectoryWidget()
		self.ui.setupUi(self)
		self.parent = mainWindow.main
		self.mainWindow = mainWindow
		self.url = url
		# set the lineEdit-URL to be as high as buttons
		self.ui.url.setSizePolicy(QtGui.QSizePolicy.MinimumExpanding,QtGui.QSizePolicy.Preferred)
		
		# set the url
		if not self.url:
			self.url = self.ui.url.text()
		
		if self.url and len(self.url) > 0:
			pass
		else:
			self.url = QtCore.QDir.homePath()
		
		self.ui.url.setText(self.url)
		
		self.ui.listView = FileManagerListView(self)
		#self.ui.listView = FileManagerTableView(self)
		#self.ui.listView = FileManagerColumnView(self)
		#self.ui.listView = FileManagerTreeView(self)
		
		self.layout().addWidget(self.ui.listView)
		
		# name the tab as current folder name
		qdir = QtCore.QDir(self.url)
		tabName = qdir.dirName()
		if not tabName:
			tabName = '/'
		
		if newTab:
			index = self.parent.addTab(self, tabName)
			self.parent.setCurrentIndex(index)
		else:
			index = self.parent.currentIndex()
			self.parent.removeTab(index)
			self.parent.insertTab(index, self, tabName)
			self.parent.setCurrentIndex(index)
		
		QtCore.QObject.connect(self.ui.newTab,QtCore.SIGNAL("clicked()"), self.mainWindow.new_tab)
		QtCore.QObject.connect(self.ui.back,QtCore.SIGNAL("clicked()"), self.mainWindow.back)
		QtCore.QObject.connect(self.ui.next,QtCore.SIGNAL("clicked()"), self.mainWindow.next)
		QtCore.QObject.connect(self.ui.close,QtCore.SIGNAL("clicked()"), self.mainWindow.close_tab)
		QtCore.QObject.connect(self.ui.up,QtCore.SIGNAL("clicked()"), self.mainWindow.up_clicked)
		QtCore.QObject.connect(self.ui.home,QtCore.SIGNAL("clicked()"), self.mainWindow.home_clicked)
		QtCore.QObject.connect(self.ui.url,QtCore.SIGNAL("returnPressed()"), self.mainWindow.url_handler)
		
		QtCore.QObject.connect(self.ui.reload,QtCore.SIGNAL("clicked()"), self.reload_items)
		QtCore.QObject.connect(self.ui.listView,QtCore.SIGNAL("activated (const QModelIndex&)"), self.activated)
		QtCore.QObject.connect(self.ui.listView,QtCore.SIGNAL("customContextMenuRequested (const QPoint&)"), self.context_menu)
		
		QtCore.QMetaObject.connectSlotsByName(self)
	
	def reload_items(self):
		"""
		The reload button slot
		"""
		directoryWidget(parent=self.parent, url=self.url, mainWindow=self.mainWindow, newTab=False)
	
	def context_menu(self, points):
		"""
		Item context menu (right click menu)
		"""
		print 'Menu'
		
		item = self.ui.listView.indexAt(points)
		if item:
			self.appDB = {'URL': self.ui.listView.model.filePath(item)}
			currentDir = unicode(self.ui.url.text())
			url = join(currentDir, unicode(item.data().toString()))
			meta = gnome_meta.get_meta_info(url)
			
			menu = ContextMenu(self, appDB=self.appDB)
			# some default actions
			menu.addAction('Open in new tab')
			
			if meta and len(meta) > 1 and meta['default_app']:
				print 'GNOME'
				menu.addSeparator()
				
				i = mime.get_icon(meta['default_app'][0])
				if i:
					i = QtGui.QIcon(i)
					menu.addAction(i, meta['default_app'][1].decode('utf-8'))
				else:
					menu.addAction(meta['default_app'][1].decode('utf-8'))
				
				self.appDB[meta['default_app'][1].decode('utf-8')] = meta['default_app'][2]
				
				if meta['other_apps'] and len(meta['other_apps']) > 1:
					for application in meta['other_apps']:
						i =  mime.get_icon(application[0])
						if i:
							i = QtGui.QIcon(i)
							menu.addAction(i, application[1].decode('utf-8'))
						else:
							menu.addAction(application[1].decode('utf-8'))
						self.appDB[application[1].decode('utf-8')] = application[2]
			else:
				meta = gio_meta.get_meta_info(url)
				if meta and len(meta) > 0:
					print 'GIO'
					menu.addSeparator()
					for application in meta:
						menu.addAction(application['name'].decode('utf-8'))
						self.appDB[application['name'].decode('utf-8')] = application['exec']
				else:
					print 'BD'
			pos = self.ui.listView.mapToGlobal(points)
			menu.exec_(pos)
		
	
	def activated(self, index):
		"""
		Handle clicking on files and folders
		"""
		if index.isValid():
			url = join(unicode(self.url), unicode(index.data().toString()))
			self.mainWindow.url_handler(url=url)

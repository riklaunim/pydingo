# -*- coding: utf-8 -*-
from os.path import isfile, isdir, join
import shutil

from PyQt4 import QtCore, QtGui

from directoryWidget import Ui_DirectoryWidget
from utils import gnome_meta, gio_meta

from utils import mime

class FileManagerModel(QtGui.QDirModel):
	def __init__(self, parent=None):
		"""
		Custom QDirModel handling Drag & Drop
		"""
		self.parent = parent
		super(FileManagerModel, self).__init__(parent)
	
	def flags(self, index):
		"""
		Enable drops of elements on folders
		"""
		if index.isValid() and self.isDir(index):
			return QtCore.Qt.ItemIsDropEnabled | QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsDragEnabled
		else:
			return QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsDragEnabled
	
	def dropMimeData(self, data, action, row, column, parent):
		"""
		Dropping elements on folders
		"""
		currentDir = unicode(self.parent.ui.url.text())
		dst = join(currentDir, unicode(parent.data().toString()))
		items = data.urls()
		if len(items) > 0 and isdir(dst):
			MOVE = 'Move'
			COPY = 'Copy'
			CANCEL = 'Cancel'
			itms = ''
			for i in items:
				itms += '- %s\n' % i.toLocalFile()
			
			message = QtGui.QMessageBox(self.parent)
			message.setText('What to do with selected items?')
			message.setWindowTitle('PyDingo File Manager')
			message.setIcon(QtGui.QMessageBox.Question)
			message.addButton(MOVE, QtGui.QMessageBox.AcceptRole)
			message.addButton(COPY, QtGui.QMessageBox.AcceptRole)
			message.addButton(CANCEL, QtGui.QMessageBox.RejectRole)
			message.setDetailedText(itms)
			message.exec_()
			response = message.clickedButton().text()
			
			if response == MOVE:
				for i in items:
					src = unicode(i.toLocalFile())
					if isdir(src):
						# If we move/copy a dir the destination must have it's name at the end
						qdir = QtCore.QDir(src)
						dst = join(dst, unicode(qdir.dirName()))
					else:
						dst = join(currentDir, unicode(parent.data().toString()))
					
					try:
						shutil.move(src, dst)
					except:
						print 'error'
						return False
				self.parent.reload_items()
			
			if response == COPY:
				for i in items:
					src = unicode(i.toLocalFile())
					if isfile(src):
						dst = join(currentDir, unicode(parent.data().toString()))
						try:
							shutil.copy(src, dst)
						except:
							print 'error'
							return False
					else:
						# If we move/copy a dir the destination must have it's name at the end
						qdir = QtCore.QDir(src)
						dst = join(dst, unicode(qdir.dirName()))
						try:
							shutil.copytree(src, dst)
						except:
							print 'error'
							return False
			return True
		return False


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
		
		# item list settings
		self.ui.listView.setResizeMode(QtGui.QListView.Adjust)
		self.ui.listView.setWordWrap(True)
		self.ui.listView.setWrapping(True)
		self.ui.listView.setIconSize(QtCore.QSize(48, 48))
		self.ui.listView.setDragEnabled(True)
		self.ui.listView.setAcceptDrops(True)
		self.ui.listView.setDropIndicatorShown(True)
		self.ui.listView.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
		self.ui.listView.setDragDropMode(QtGui.QAbstractItemView.DragDrop)
		self.ui.listView.setSelectionMode(QtGui.QAbstractItemView.ContiguousSelection)
		
		# QDirModel settings
		self.model = FileManagerModel(self)
		self.model.setFilter(QtCore.QDir.AllEntries | QtCore.QDir.NoDotAndDotDot)
		self.model.setSorting(QtCore.QDir.DirsFirst)
		#self.model.setReadOnly(False)
		self.ui.listView.setModel(self.model)
		
		# set the url
		if not self.url:
			self.url = self.ui.url.text()
		
		if self.url and len(self.url) > 0:
			pass
		else:
			self.url = QtCore.QDir.homePath()
		
		self.ui.url.setText(self.url)
		# set the URL for the model
		self.ui.listView.setRootIndex(self.model.index(self.url))
		
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
		directoryWidget(parent=self.parent, url=self.url, mainWindow=self.mainWindow, newTab=False)
	
	def context_menu(self, points):
		print 'Menu'
		item = self.ui.listView.indexAt(points)
		if item:
			currentDir = unicode(self.ui.url.text())
			url = join(currentDir, unicode(item.data().toString()))
			meta = gnome_meta.get_meta_info(url)
			
			menu = QtGui.QMenu(self)
			# some default actions
			menu.addAction('Open in new tab')
			
			if meta and len(meta) > 1 and meta['default_app']:
				print 'GNOME'
				menu.addSeparator()
				menu.addAction(meta['default_app'][1].decode('utf-8'))
				if meta['other_apps'] and len(meta['other_apps']) > 1:
					for application in meta['other_apps']:
						menu.addAction(application[1].decode('utf-8'))
			else:
				meta = gio_meta.get_meta_info(url)
				if len(meta) > 0:
					print 'GIO'
					menu.addSeparator()
					for application in meta:
						menu.addAction(application['name'].decode('utf-8'))
				else:
					print 'BD'
			pos = self.ui.listView.mapToGlobal(points)
			menu.exec_(pos)
		
	
	def activated(self, index):
		print 'Item Activated'
		if index.isValid():
			url = join(unicode(self.url), unicode(index.data().toString()))
			self.mainWindow.url_handler(url=url)

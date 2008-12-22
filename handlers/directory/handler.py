# -*- coding: utf-8 -*-
from os.path import isfile, isdir, join
import shutil

from PyQt4 import QtCore, QtGui

from directoryWidget import Ui_DirectoryWidget
from utils import gnome_meta, gio_meta

from utils import mime

class FileManagerWidget(QtGui.QListWidget):
	def __init__(self, parent=None,):
		"""
		QListWidget with handling of mouse events - left and right clicks
		"""
		super(FileManagerWidget, self).__init__(parent)
		
		# configure the items list
		self.setViewMode(QtGui.QListView.IconMode)
		self.setResizeMode(QtGui.QListView.Adjust)
		self.setGridSize(QtCore.QSize(80, 95))
		self.setIconSize(QtCore.QSize(48, 48))
		self.setDragDropMode(QtGui.QAbstractItemView.DragDrop)
		self.setSelectionMode(QtGui.QAbstractItemView.ContiguousSelection)
		self.setWordWrap(True)
		self.setWrapping(True)
		
		self.parent = parent
		
		QtCore.QMetaObject.connectSlotsByName(self)
	
	def contextMenuEvent(self, event):
		"""
		Handle context menu for items and for "blank space"
		* for item display suggested apps and some default actions
		* for "blank space" display default actions for current directory like mkdir
		"""
		print 'menu'
		item = self.itemAt(event.x(), event.y())
		# context menu for items
		if item:
			currentDir = unicode(self.parent.ui.url.text())
			url = join(currentDir, unicode(item.text()))
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
			menu.exec_(event.globalPos())
	

	def mouseReleaseEvent(self, event):
		"""
		Handle the event.
		for left click-release - go to the file/directory
		"""
		items = self.selectedItems()
		if len(items) < 2:
			button = event.button()
			item = self.itemAt(event.x(), event.y())
			if item:
				self.setCurrentItem(item)
				if button == 1:
					self.item_clicked()
	

	def dropEvent(self, event):
		"""
		Handle drag and droping files/folders on other folders
		to copy or move them to that folder
		"""
		print 'Drop'
		itemAt = self.itemAt(event.pos())
		currentDir = unicode(self.parent.ui.url.text())
		dst = join(currentDir, unicode(itemAt.text()))
		if itemAt and isdir(dst):
			items = self.selectedItems()
			if len(items) > 0:
				MOVE = 'Move'
				COPY = 'Copy'
				CANCEL = 'Cancel'
				itms = ''
				for i in items:
					itms += '- %s\n' % i.text()
				
				message = QtGui.QMessageBox(self)
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
						src = join(currentDir, unicode(i.text()))
						if isdir(src):
							# If we move/copy a dir the destination must have it's name at the end
							dst = join(currentDir, unicode(itemAt.text()), unicode(i.text()))
						else:
							dst = join(currentDir, unicode(itemAt.text()))
						shutil.move(src, dst)
							
					self.parent.reload_items()
				if response == COPY:
					for i in items:
						src = join(currentDir, unicode(i.text()))
						if isfile(src):
							dst = join(currentDir, unicode(itemAt.text()))
							shutil.copy(src, dst)
						else:
							# If we move/copy a dir the destination must have it's name at the end
							dst = join(currentDir, unicode(itemAt.text()), unicode(i.text()))
							shutil.copytree(src, dst)
				
	
	#def mousePressEvent(self, event):
		#"""
		#Handle the event.
		#* for left clicks - ability to drag item
		#* for right clicks - show context menu
		#"""
		#button = event.button()
		#item = self.itemAt(event.x(), event.y())
		#if item:
			#self.setCurrentItem(item)
			#if button == 1:
				#print 'LEFT DRAG'
		#if button == 2:
			#print 'Right'
	
	def item_clicked(self):
		"""
		File or folder clicked
		"""
		item = self.currentItem().text()
		url = join(unicode(self.parent.ui.url.text()),unicode(item))
		if isfile(url):
			self.parent.mainWindow.url_handler(url=url)
		elif isdir(url):
			q = QtCore.QDir(url + u'/.')
			if q.isReadable():
				self.parent.mainWindow.url_handler(url=url)
			else:
				print 'NOT READABLE'
		else:
			print u'NOT A FILE OR DIRECTORY %s' % unicode(url)


class directoryWidget(QtGui.QWidget):
	def __init__(self, parent=None, url=False, mainWindow=False, newTab=False):
		super(directoryWidget, self).__init__(mainWindow.main)
		self.ui = Ui_DirectoryWidget()
		self.ui.setupUi(self)
		layout = self.layout()
		self.ui.items = FileManagerWidget(parent=self)
		layout.addWidget(self.ui.items)
		self.parent = mainWindow.main
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
		self.url = url
		
		# name the tab as current folder name
		tabName = qdir.dirName()
		if not tabName:
			tabName = '/'
		
		qdir.setFilter(QtCore.QDir.AllEntries | QtCore.QDir.NoDotAndDotDot)
		qdir.setSorting(QtCore.QDir.DirsFirst)
		qdirs = qdir.entryList()
		for d in qdirs:
			itm = QtGui.QListWidgetItem(d)
			itm.setToolTip(u'<b>Filename</b>: %s' % d)
			if isdir(unicode(url)+u'/'+unicode(d)):
				q = QtCore.QDir(unicode(url)+u'/'+unicode(d) + u'/.')
				if q.isReadable():
					itm.setIcon(QtGui.QIcon('media/mime_icons/folder_blue.png'))
					itm.setFlags(QtCore.Qt.ItemIsDropEnabled | QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEditable | QtCore.Qt.ItemIsDragEnabled | QtCore.Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsEnabled)
				else:
					itm.setIcon(QtGui.QIcon('media/mime_icons/folder_locked.png'))
			else:
				mimetype = unicode(mime.get_mime(url+u'/'+d))
				
				if mime.is_plaintext(mimetype):
					itm.setIcon(QtGui.QIcon('media/mime_icons/ascii.png'))
				elif mimetype == 'application/pdf':
					itm.setIcon(QtGui.QIcon('media/mime_icons/pdf.png'))
				elif mimetype.startswith('image'):
					itm.setIcon(QtGui.QIcon('media/mime_icons/image.png'))
				elif mimetype.startswith('audio'):
					itm.setIcon(QtGui.QIcon('media/mime_icons/audio-x-generic.png'))
				elif mimetype.find('application/x-font-ttf') != -1:
					itm.setIcon(QtGui.QIcon('media/mime_icons/font_truetype.png'))
				elif mimetype.startswith('video'):
					itm.setIcon(QtGui.QIcon('media/mime_icons/video.png'))
				elif mimetype.find('zip') != -1 or mimetype.find('rar') != -1 or mimetype.find('rpm') != -1 or mimetype.find('deb') != -1 or mimetype.find('tar') != -1 or mimetype.find('archive') != -1:
					itm.setIcon(QtGui.QIcon('media/mime_icons/package.png'))
				elif mimetype =='application/x-msi' or mimetype == 'application/x-ms-win-installer' or mimetype.find('executable') != -1 or mimetype == 'application/octet-stream':
					itm.setIcon(QtGui.QIcon('media/mime_icons/exec.png'))
				elif mimetype == 'application/x-sharedlib':
					itm.setIcon(QtGui.QIcon('media/mime_icons/binary.png'))
				elif mimetype.find('html') != -1:
					itm.setIcon(QtGui.QIcon('media/mime_icons/html.png'))
				elif mimetype == 'application/x-cd-image':
					itm.setIcon(QtGui.QIcon('media/mime_icons/iso.png'))
				elif mimetype == 'application/x-trash':
					itm.setIcon(QtGui.QIcon('media/mime_icons/recycled.png'))
				elif mimetype == 'application/vnd.oasis.opendocument.presentation' or mimetype.find('powerpoint') != -1:
					itm.setIcon(QtGui.QIcon('media/mime_icons/openofficeorg-20-oasis-presentation.png'))
				elif mimetype.find('spreadsheet') != -1:
					itm.setIcon(QtGui.QIcon('media/mime_icons/openofficeorg-20-oasis-spreadsheet.png'))
				elif mimetype == 'application/vnd.oasis.opendocument.graphics':
					itm.setIcon(QtGui.QIcon('media/mime_icons/openofficeorg-20-oasis-drawing.png'))
				elif mimetype == 'application/vnd.oasis.opendocument.text' or mimetype.find('msword') != -1 or mimetype == 'application/x-chm':
					itm.setIcon(QtGui.QIcon('media/mime_icons/openofficeorg-20-oasis-text.png'))
				elif mimetype.find('bytecode') != -1:
					itm.setIcon(QtGui.QIcon('media/mime_icons/bytecode.png'))
				else:
					print mimetype
					print unicode(url)+u'/'+unicode(d)
					print
					itm.setIcon(QtGui.QIcon('media/mime_icons/unknown.png'))
			self.ui.items.addItem(itm)
		
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
		
		#QtCore.QObject.connect(self.ui.items,QtCore.SIGNAL("itemClicked (QListWidgetItem *)"), self.item_clicked)
		QtCore.QMetaObject.connectSlotsByName(self)
	
	def reload_items(self):
		directoryWidget(parent=self.parent, url=self.url, mainWindow=self.mainWindow, newTab=False)

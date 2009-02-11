# -*- coding: utf-8 -*-
import sys
from os.path import isfile, isdir

from PyQt4 import QtCore, QtGui, QtWebKit

from dingo import Ui_Dingo
from utils import mime
import resources_rc

class Dingo(QtGui.QMainWindow):
	def __init__(self, parent=None):
		QtGui.QWidget.__init__(self, parent)
		self.ui = Ui_Dingo()
		self.ui.setupUi(self)
		self.setWindowState(QtCore.Qt.WindowMaximized)
		
		# setup for URL history
		self.history = {}
		self.future = {}
		# copy, cut container
		self.filemanagerContainer = []
		self.filemanagerContainerType = False
		
		# Future - docking widgets from tabs
		self.setDockNestingEnabled(True)
		self.setDockOptions(QtGui.QMainWindow.VerticalTabs)
		self.ui.dockFrame.hide()
		
		# Back button history
		self.back_bucket = {}
		
		# Set the mainFrame with QTabWidget and load welcome page
		mainFrame = self.ui.mainFrame
		mainLayout =  mainFrame.layout()
		mainLayout.setMargin(0)
		
		# create QTabWidget
		self.main = QtGui.QTabWidget()
		
		# create the starting tab
		from handlers.directory import handler
		self.tab = handler.directoryWidget(mainWindow=self)
		self.history[self.main.currentIndex()] = [unicode(self.tab.ui.url.text())]
		self.future[self.main.currentIndex()] = []
		self.tab.ui.back.setEnabled(False)
		self.tab.ui.next.setEnabled(False)
		mainLayout.addWidget(self.main)
		self.set_shortcuts()
		
		# QMenuBar actions
		QtCore.QObject.connect(self.ui.actionClose,QtCore.SIGNAL("triggered()"), self.action_close)
		QtCore.QObject.connect(self.ui.actionFile_Manager,QtCore.SIGNAL("triggered()"), self.new_tab)
		QtCore.QObject.connect(self.ui.actionWeb_Browser,QtCore.SIGNAL("triggered()"), self.new_browser)
		QtCore.QObject.connect(self.ui.actionText_Editor,QtCore.SIGNAL("triggered()"), self.new_textEditor)
		QtCore.QObject.connect(self.ui.actionAbout,QtCore.SIGNAL("triggered()"), self.about)
		
	def about(self):
		"""
		Show app info
		"""
		message = QtGui.QMessageBox(self)
		message.setTextFormat(QtCore.Qt.RichText)
		message.setText(u'<b>PyDingo File Manager 0.4 Alpha</b><br><br><b>Author</b>: Piotr "Riklaunim" Maliński<br><b>Mail</b>: <a href="mailto:riklaunim@gmail.com">riklaunim@gmail.com</a><br><b>License</b>: GPL')
		message.setWindowTitle('PyDingo 0.4')
		message.setIcon(QtGui.QMessageBox.Information)
		message.addButton('Ok', QtGui.QMessageBox.AcceptRole)
		#message.setDetailedText('Unsaved changes in: ' + self.ui.url.text())
		message.exec_()
	
	def action_close(self):
		"""
		Close the application
		"""
		self.close()
		
	def close_tab(self):
		"""
		Remove the current tab
		"""
		index = self.main.currentIndex()
		# delete URL history
		try:
			del self.history[index]
			del self.future[index]
		except:
			pass
		self.main.removeTab(index)
		if index == 0:
			# no more tabs, create a standard new one
			from handlers.directory import handler
			self.tab = handler.directoryWidget(mainWindow=self)
			self.history[self.main.currentIndex()] = [unicode(self.tab.ui.url.text())]
			self.future[self.main.currentIndex()] = []
			self.tab.ui.back.setEnabled(False)
			self.tab.ui.next.setEnabled(False)
			self.set_shortcuts()
	
	def new_tab(self):
		"""
		Create a new Tab / file manager
		"""
		from handlers.directory import handler
		self.tab = handler.directoryWidget(mainWindow=self, newTab=True)
		self.history[self.main.currentIndex()] = [unicode(self.tab.ui.url.text())]
		self.future[self.main.currentIndex()] = []
		self.tab.ui.back.setEnabled(False)
		self.tab.ui.next.setEnabled(False)
		self.set_shortcuts()
	
	def new_browser(self):
		"""
		Create a new Tab - web browser
		"""
		from handlers.http import handler
		self.tab = handler.httpWidget(mainWindow=self, newTab=True, url='http://www.google.pl')
		self.history[self.main.currentIndex()] = [unicode(self.tab.ui.url.text())]
		self.future[self.main.currentIndex()] = []
		self.tab.ui.back.setEnabled(False)
		self.tab.ui.next.setEnabled(False)
		self.set_shortcuts()
	
	def new_textEditor(self):
		"""
		Create a new Tab - text editor
		"""
		from handlers.file import handler
		self.tab = handler.fileWidget(mainWindow=self, newTab=True)
		self.history[self.main.currentIndex()] = [unicode(self.tab.ui.url.text())]
		self.future[self.main.currentIndex()] = []
		self.tab.ui.back.setEnabled(False)
		self.tab.ui.next.setEnabled(False)
		self.set_shortcuts()
	
	
	def up_clicked(self):
		"""
		Up Arrow clicked - go on level up
		* leave a file and go to folder view - not here
		* go on folder up
		"""
		self.tab = self.main.currentWidget()
		index = self.main.currentIndex()
		uri = self.tab.ui.url.text()
		if isdir(uri) or isfile(uri):
			q = QtCore.QDir(uri)
			if q.cdUp():
				# clean "next" history
				self.future[index] = []
				self.tab.ui.next.setEnabled(False)
				self.url_handler(url=q.canonicalPath())
			if q.isRoot():
				self.tab.ui.up.setEnabled(False)
		elif unicode(uri).startswith('http://') or unicode(uri).startswith('www'):
			uri = unicode(uri).replace('http://', '')
			elems = uri[:-1].split('/')
			if len(elems) > 1:
				del elems[-1]
				uri = '/'.join(elems)
				uri = 'http://%s' % uri
				# clean "next" history
				self.future[index] = []
				self.tab.ui.next.setEnabled(False)
				self.url_handler(url=uri)
	
	def home_clicked(self):
		"""
		Home icon clicked
		"""
		url = QtCore.QDir.homePath()
		self.url_handler(url=url)
	
	def back(self):
		"""
		Go back one url
		"""
		index = self.main.currentIndex()
		self.tab = self.main.currentWidget()
		
		if len(self.history[index]) > 1:
			self.future[index].append(self.history[index][-1])
			del self.history[index][-1]
			
			if len(self.future[index]) > 0:
				self.tab.ui.next.setEnabled(True)
			
			self.url_handler(url=self.history[index][-1])
		else:
			self.tab.ui.back.setEnabled(False)
	
	def next(self):
		"""
		Go to next URL in history
		"""
		index = self.main.currentIndex()
		self.tab = self.main.currentWidget()
		
		if len(self.future[index]) > 0:
			self.history[index].append(self.future[index][-1])
			del self.future[index][-1]
			
			if len(self.history[index]) > 1:
				self.tab.ui.back.setEnabled(True)
			
			self.url_handler(url=self.history[index][-1])
		else:
			self.tab.ui.next.setEnabled(False)
	
	def url_handler(self, url=False, newTab=False):
		"""
		Handle URL from self.url
		
		ToDo:
			Write a pluggable URL handler for web, file browsing, and special tabs
		"""
		self.tab = self.main.currentWidget()
		if not url:
			url = self.tab.ui.url.text()
		
		self.tab.ui.up.setEnabled(True)
		index = self.main.currentIndex()
		
		if isdir(url):
			q = QtCore.QDir(url)
			if q.isRoot():
				self.tab.ui.up.setEnabled(False)
			from handlers.directory import handler
			self.tab = handler.directoryWidget(url=url, mainWindow=self, newTab=newTab)
		elif isfile(url):
			mimetype = mime.get_mime(url)
			if mimetype and mime.is_plaintext(mimetype):
				from handlers.file import handler
				self.tab = handler.fileWidget(url=url, mainWindow=self, mime=mimetype, newTab=newTab)
			else:
				#from handlers.metafile import handler
				#self.tab = handler.metafileWidget(self.main, url=url, mainWindow=self, newTab=newTab)
				q = QtGui.QDesktopServices()
				q.openUrl(QtCore.QUrl(url))
		elif unicode(url).startswith('http://') or unicode(url).startswith('www'):
			if unicode(url).startswith('www'):
				url = 'http://%s' % unicode(url)
			from handlers.http import handler
			self.tab = handler.httpWidget(url=url, mainWindow=self, newTab=newTab)
		else:
			"""
			ToDo:
				- clean the core here, make elif for web urls
				- make a generic url to handler executer here
				- make a default - no plugin found for this url widget/page
			"""
			routing = unicode(url)
			print routing
			if isfile(routing):
				q = QtGui.QDesktopServices()
				q.openUrl(QtCore.QUrl.fromLocalFile(routing))
		
		# URL history
		if self.history.has_key(index):
			if len(self.history[index]) < 2:
				self.tab.ui.back.setEnabled(False)
			# add URL if he isn't in the history
			if self.history[index].count(unicode(url)) < 1:
				self.tab.ui.back.setEnabled(True)
				self.history[index].append(unicode(url))
				
				# if users clicks on an item that is somewhere in future
				# delete it as he is on a new browsing path
				if self.future.has_key(index) and self.future[index].count(unicode(url)) < 1:
					self.future[index] = []
					self.tab.ui.next.setEnabled(False)
		else:
			self.tab.ui.back.setEnabled(False)
			self.history[index] = [unicode(url)]
		
		# If there are future entries - enable next button
		if self.future.has_key(index) and len(self.future[index]) > 0:
			self.tab.ui.next.setEnabled(True)
		else:
			self.future[index] = []
			self.tab.ui.next.setEnabled(False)
		
		if newTab:
			# set basic settings for new tabs with non-default URL
			self.history[self.main.currentIndex()] = [unicode(self.tab.ui.url.text())]
			self.future[self.main.currentIndex()] = []
			self.tab.ui.back.setEnabled(False)
			self.tab.ui.next.setEnabled(False)
		
		self.set_shortcuts()
		
	def set_shortcuts(self):
		"""
		Set keyboard shortcuts for core buttons
		"""
		self.tab = self.main.currentWidget()
		
		close = QtGui.QKeySequence(QtGui.QKeySequence.Close)
		self.tab.ui.close.setShortcut(close)
		
		ntab = QtGui.QKeySequence(QtGui.QKeySequence.AddTab)
		self.tab.ui.newTab.setShortcut(ntab)
		
		back = QtGui.QKeySequence(QtGui.QKeySequence.Back)
		self.tab.ui.back.setShortcut(back)
		
		next = QtGui.QKeySequence(QtGui.QKeySequence.Forward)
		self.tab.ui.next.setShortcut(next)
		
		home = QtGui.QKeySequence(QtGui.QKeySequence.MoveToStartOfLine)
		self.tab.ui.home.setShortcut(home)

if __name__ == "__main__":
	app = QtGui.QApplication(sys.argv)
	myapp = Dingo()
	myapp.show()
	sys.exit(app.exec_())

# -*- coding: utf-8 -*-
import sys
from os.path import isfile, isdir, expanduser

from PyQt4 import QtCore, QtGui, QtWebKit

from dingo import Ui_Dingo
from utils import mime

class Dingo(QtGui.QMainWindow):
	def __init__(self, parent=None):
		QtGui.QWidget.__init__(self, parent)
		self.ui = Ui_Dingo()
		self.ui.setupUi(self)
		
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
		self.tab = handler.directoryWidget(self.main, mainWindow=self)
		mainLayout.addWidget(self.main)
	
	def close_tab(self):
		"""
		Remove the current tab
		"""
		index = self.main.currentIndex()
		self.main.removeTab(index)
		if index == 0:
			from handlers.directory import handler
			handler.directoryWidget(self.main, mainWindow=self)
	
	def new_tab(self):
		"""
		Create a new Tab
		"""
		from handlers.directory import handler
		handler.directoryWidget(self.main, mainWindow=self, newTab=True)
	
	def up_clicked(self):
		"""
		Up Arrow clicked - go on level up
		* leave a file and go to folder view - not here
		* go on folder up
		"""
		self.tab = self.main.currentWidget()
		uri = unicode(self.tab.ui.url.text()).split('/')
		if len(uri) > 2:
			if  len(uri[-1]) > 0:
				del uri[-1]
			else:
				del uri[-1]
				del uri[-2]
			uri = '/'.join(uri)
		else:
			uri = '/'
		self.tab.ui.url.setText(uri)
		self.url_handler()
	
	def home_clicked(self):
		"""
		Home icon clicked
		"""
		uri = expanduser('~')
		self.tab.ui.url.setText(uri)
		self.url_handler()
	
	def back(self):
		"""
		Go back one url
		"""
		#self.t = self.main.currentIndex()
		#if self.t:
			#tab_id = unicode(self.t)
			#if self.back_bucket.has_key(tab_id) and len(self.back_bucket[tab_id]) > 1:
				#del self.back_bucket[tab_id][-1]
				#self.url_handler(url=self.back_bucket[tab_id][-1])
		
		#print self.back_bucket
		#self.tab = self.main.currentWidget()
		#if self.tab:
			#print self.tab.ui.back.menu()
			#print 'a'
			#self.tab.ui.back.showMenu()
		return False
	
	def update_back_bucket(self, newurl):
		"""
		Handle adding new items to url history
		"""
		self.tab = self.main.currentWidget()
		if self.tab:
			if not self.tab.ui.back.menu():
				menu = QtGui.QMenu()
				menu.addAction(newurl)
			else:
				menu = self.tab.ui.back.menu()
				menu.addAction(newurl)
			return menu
		return False
		#if self.t:
			#tab_id = unicode(self.t)
			#if not self.back_bucket.has_key(tab_id):
				#self.back_bucket[tab_id] = []
			#self.back_bucket[tab_id].append(newurl)
			## keep only last 10 urls
			#if len(self.back_bucket[tab_id]) > 10:
				#self.back_bucket[tab_id] = self.back_bucket[tab_id][-10:-1]
		
	
	def url_handler(self, url=False):
		"""
		Handle URL from self.url
		
		ToDo:
			Write a pluggable URL handler for web, file browsing, and special tabs
		"""

		w = self.main.currentWidget()
		if not url:
			url = w.ui.url.text()
		
		if isdir(url):
			from handlers.directory import handler
			self.tab = handler.directoryWidget(self.main, url=url, mainWindow=self)
		elif isfile(url):
			ext = url.split('.')[-1]
			mimetype = unicode(mime.get_mime(url))
			if mimetype and mime.is_plaintext(mimetype):
				from handlers.file import handler
				self.tab = handler.fileWidget(self.main, url=url, mainWindow=self)
			else:
				print 'BINARY: %s' % mimetype
		else:
			"""
			ToDo:
				- clean the core here, make elif for web urls
				- make a generic url to handler executer here
				- make a default - no plugin found for this url widget/page
			"""
			url_nodes = url.split(':')
			if len(url_nodes) > 1:
				if url_nodes[0] == 'http':
					from handlers.http import handler
					self.tab = handler.handle(self.main, url)
			else:
				if url[0:3] == 'www':
					from handlers.http import handler
					self.tab = handler.handle(self.main, url)
				else:
					print 'nieznany'

if __name__ == "__main__":
	app = QtGui.QApplication(sys.argv)
	myapp = Dingo()
	myapp.show()
	sys.exit(app.exec_())

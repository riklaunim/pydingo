# -*- coding: utf-8 -*-
# Web browser based on qt-webkit

from PyQt4 import QtCore, QtGui
from httpWidget import Ui_HttpWidget

class httpWidget(QtGui.QWidget):
	def __init__(self, parent=None, url=False, mainWindow=False, newTab=False):
		super(httpWidget, self).__init__(mainWindow.main)
		self.ui = Ui_HttpWidget()
		self.ui.setupUi(self)
		self.parent = mainWindow.main
		self.mainWindow = mainWindow
		# set the lineEdit-URL to be as high as buttons
		self.ui.url.setSizePolicy(QtGui.QSizePolicy.MinimumExpanding,QtGui.QSizePolicy.Preferred)
		
		# history buttons:
		self.ui.back.setEnabled(False)
		self.ui.next.setEnabled(False)
		
		# set the url
		if not url:
			url = self.ui.url.text()
		
		self.ui.url.setText(url)
		
		# name the tab as current folder name
		tabName = url
		
		# load page
		self.ui.webView.setUrl(QtCore.QUrl(url))
		
		if newTab:
			index = self.parent.addTab(self, tabName)
			self.parent.setCurrentIndex(index)
		else:
			index = self.parent.currentIndex()
			self.parent.removeTab(index)
			self.parent.insertTab(index, self, tabName)
			self.parent.setCurrentIndex(index)
		
		QtCore.QObject.connect(self.ui.newTab,QtCore.SIGNAL("clicked()"), self.mainWindow.new_tab)
		QtCore.QObject.connect(self.ui.close,QtCore.SIGNAL("clicked()"), self.mainWindow.close_tab)
		QtCore.QObject.connect(self.ui.up,QtCore.SIGNAL("clicked()"), self.mainWindow.up_clicked)
		QtCore.QObject.connect(self.ui.home,QtCore.SIGNAL("clicked()"), self.mainWindow.home_clicked)
		QtCore.QObject.connect(self.ui.url,QtCore.SIGNAL("returnPressed()"), self.mainWindow.url_handler)
		
		# let use WebKit history for better quality of moving next/back
		QtCore.QObject.connect(self.ui.back,QtCore.SIGNAL("clicked()"), self.back)
		QtCore.QObject.connect(self.ui.next,QtCore.SIGNAL("clicked()"), self.next)
		
		QtCore.QObject.connect(self.ui.webView,QtCore.SIGNAL("linkClicked (const QUrl&)"), self.link_clicked)
		QtCore.QObject.connect(self.ui.webView,QtCore.SIGNAL("urlChanged (const QUrl&)"), self.link_clicked)
		QtCore.QObject.connect(self.ui.webView,QtCore.SIGNAL("loadProgress (int)"), self.load_progress)
		QtCore.QObject.connect(self.ui.webView,QtCore.SIGNAL("titleChanged (const QString&)"), self.title_changed)
		QtCore.QObject.connect(self.ui.reload,QtCore.SIGNAL("clicked()"), self.reload_page)
		QtCore.QObject.connect(self.ui.stop,QtCore.SIGNAL("clicked()"), self.stop_page)
		
		
		QtCore.QMetaObject.connectSlotsByName(self)
	
	def back(self):
		"""
		Back button clicked, go one page back
		"""
		page = self.ui.webView.page()
		history = page.history()
		history.back()
		if history.canGoBack():
			self.ui.back.setEnabled(True)
		else:
			self.ui.back.setEnabled(False)
	
	def next(self):
		"""
		Next button clicked, go to next page
		"""
		page = self.ui.webView.page()
		history = page.history()
		history.forward()
		if history.canGoForward():
			self.ui.next.setEnabled(True)
		else:
			self.ui.next.setEnabled(False)

	
	def stop_page(self):
		"""
		Stop loading the page
		"""
		self.ui.webView.stop()
	
	def title_changed(self, title):
		"""
		Web page title changed - change the tab name
		"""
		index = self.parent.currentIndex()
		self.parent.setTabText(index, title)
	
	def reload_page(self):
		"""
		Reload the web page
		"""
		self.ui.webView.setUrl(QtCore.QUrl(self.ui.url.text()))
	
	def link_clicked(self, url):
		"""
		Update the URL if a link on a web page is clicked
		"""
		page = self.ui.webView.page()
		history = page.history()
		if history.canGoBack():
			self.ui.back.setEnabled(True)
		else:
			self.ui.back.setEnabled(False)
		if history.canGoForward():
			self.ui.next.setEnabled(True)
		else:
			self.ui.next.setEnabled(False)
		
		self.ui.url.setText(url.toString())
		
		url = url.toString()
		index = self.parent.currentIndex()
		if self.mainWindow.history.has_key(index):
			if len(self.mainWindow.history[index]) < 2:
				self.mainWindow.tab.ui.back.setEnabled(False)
			# add URL if he isn't in the history
			if self.mainWindow.history[index].count(unicode(url)) < 1:
				self.mainWindow.tab.ui.back.setEnabled(True)
				self.mainWindow.history[index].append(unicode(url))
				
				# if users clicks on an item that is somewhere in future
				# delete it as he is on a new browsing path
				if self.mainWindow.future.has_key(index) and self.mainWindow.future[index].count(unicode(url)) < 1:
					self.mainWindow.future[index] = []
					self.mainWindow.tab.ui.next.setEnabled(False)
		else:
			self.mainWindow.tab.ui.back.setEnabled(False)
			self.mainWindow.history[index] = [unicode(url)]
	
	def load_progress(self, load):
		"""
		Page load progress
		"""
		if load == 100:
			self.ui.stop.setEnabled(False)
		else:
			self.ui.stop.setEnabled(True)
	
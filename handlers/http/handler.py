# -*- coding: utf-8 -*-
from PyQt4 import QtCore, QtGui, QtWebKit

def handle(tab, url):
	"""
	Handle a web page request
	"""
	widget = QtWebKit.QWebView()
	widget.setUrl(QtCore.QUrl(url))
	
	index = tab.currentIndex()
	tab.removeTab(index)
	tab.insertTab(index, widget, 'Witaj')
	tab.setCurrentIndex(index)
	return True

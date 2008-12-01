# -*- coding: utf-8 -*-
import codecs
from os import listdir
from os.path import isfile, isdir, expanduser, join

from PyQt4 import QtCore, QtGui, Qsci

from metafileWidget import Ui_MetafileWidget
from utils import mime
import hachoir_meta
import gnome_meta

class metafileWidget(QtGui.QWidget):
	def __init__(self, parent=None, url=False, mainWindow=False, newTab=False):
		super(metafileWidget, self).__init__(parent)
		self.ui = Ui_MetafileWidget()
		self.ui.setupUi(self)
		
		# set the lineEdit-URL to be as high as buttons
		self.ui.url.setSizePolicy(QtGui.QSizePolicy.MinimumExpanding,QtGui.QSizePolicy.Preferred)
		# set the "Actions" groupBox to max size
		self.ui.splitter.setStretchFactor(0,1)
		
		self.parent = parent
		self.mainWindow = mainWindow
		
		if not url:
			url = self.ui.url.text()
		
		# use filename for tab name
		tabName = url.split('/')
		tabName = tabName[-1]
		
		# set the URL
		self.ui.url.setText(url)
		self.mainWindow.update_back_bucket(unicode(url))
		
		meta = hachoir_meta.get_meta_info(url)
		if meta and len(meta) > 0:
			text = '\n<br />'.join(meta)
			no_meta = False
		else:
			mimetype = unicode(mime.get_mime(url))
			text = '- Mime: %s<br />' % mimetype
			no_meta = True
		textWidget = QtGui.QTextBrowser()
		textWidget.setHtml(text)
		index = self.ui.metaInfo.currentIndex()
		self.ui.metaInfo.removeItem(index)
		self.ui.metaInfo.insertItem(index, textWidget, 'File Info')
		self.ui.metaInfo.setCurrentIndex(index)
		
		meta = gnome_meta.get_meta_info(url)
		app_name = False
		if meta and len(meta) > 0:
			text = u'<b>Mime</b>: %s<br />' % meta['mime']
			text += u'<b>Description</b>: %s<br />' % meta['description'].decode('utf-8')
			if meta['default_app'] and len(meta['default_app']) > 0:
				app_desktop = meta['default_app'][0]
				app_name = meta['default_app'][1]
				app_bin = meta['default_app'][2]
				"""
				ToDo: execute with application
				"""
				text += u'<b>Default application</b>: %s<br />' % app_name
			if meta['other_apps'] and len(meta['other_apps']) > 0:
				text += u'<b>Other applications</b>:<br />'
				for app in meta['other_apps']:
					if app[1] != app_name:
						text += u'- %s<br />' % app[1]
			
		textWidget = QtGui.QTextBrowser()
		textWidget.setHtml(text)
		index  = self.ui.metaInfo.addItem(textWidget, 'GNOME')
		if no_meta or app_name:
			self.ui.metaInfo.setCurrentIndex(index)
			
		
		# set the tab
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
	
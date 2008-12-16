# -*- coding: utf-8 -*-
import codecs
from os import listdir
from os.path import isfile, isdir, expanduser, join

from PyQt4 import QtCore, QtGui, Qsci

from metafileWidget import Ui_MetafileWidget
from utils import mime
from utils import hachoir_meta, gnome_meta, gio_meta

class metafileWidget(QtGui.QWidget):
	def __init__(self, parent=None, url=False, mainWindow=False, newTab=False):
		super(metafileWidget, self).__init__(mainWindow.main)
		self.ui = Ui_MetafileWidget()
		self.ui.setupUi(self)
		
		# set the lineEdit-URL to be as high as buttons
		self.ui.url.setSizePolicy(QtGui.QSizePolicy.MinimumExpanding,QtGui.QSizePolicy.Preferred)
		
		self.ui.metaInfo = QtGui.QToolBox()
		self.ui.splitter.insertWidget(1, self.ui.metaInfo)
		# set the "Actions" groupBox to max size
		self.ui.splitter.setStretchFactor(0,1)
		
		self.parent = mainWindow.main
		self.mainWindow = mainWindow
		
		if not url:
			url = self.ui.url.text()
		
		# use filename for tab name
		tabName = url.split('/')
		tabName = tabName[-1]
		
		# set the URL
		self.ui.url.setText(url)
		
		# sample of what this widget could do - if it's image: display it
		mimetype = unicode(mime.get_mime(url))
		if isfile(url) and mimetype.startswith('image'):
			img = QtGui.QPixmap(url)
			img = img.scaled(300, 300, QtCore.Qt.KeepAspectRatio)
			label = QtGui.QLabel()
			label.setPixmap(img)
			
			l = QtGui.QHBoxLayout()
			l.addWidget(label)
			self.ui.actions.setLayout(l)
		
		"""
		This will have to look better, use QTreeWidget
		"""
		meta = hachoir_meta.get_meta_info(url)
		if meta and len(meta) > 0:
			text = '\n<br />'.join(meta)
			no_meta = False
		else:
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
		text = False
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
			if meta['other_apps'] and len(meta['other_apps']) > 1:
				text += u'<b>Other applications</b>:<br />'
				for app in meta['other_apps']:
					if app[1] != app_name:
						text += u'- %s<br />' % app[1]
		if text:
			textWidget = QtGui.QTextBrowser()
			textWidget.setHtml(text)
			index  = self.ui.metaInfo.addItem(textWidget, 'GNOME')
			if no_meta or app_name:
				self.ui.metaInfo.setCurrentIndex(index)
		
		meta = gio_meta.get_meta_info(url)
		text = False
		if meta and len(meta) > 0:
			text = ''
			for app in meta:
				text += u'<b>Application</b>: %s<br />' % app['name']
				if app['description']:
					text += u'<b>Description</b>: %s<br />' % app['description'].decode('utf-8')
				text += u'<b>Executable</b>: %s<br /><br />' % app['exec']
			
		if text:
			textWidget = QtGui.QTextBrowser()
			textWidget.setHtml(text)
			index  = self.ui.metaInfo.addItem(textWidget, 'GNOME / GIO')
			if no_meta and not app_name:
				self.ui.metaInfo.setCurrentIndex(index)
		
		
		# set the tab
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
		QtCore.QMetaObject.connectSlotsByName(self)
	
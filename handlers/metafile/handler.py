# -*- coding: utf-8 -*-
import codecs
from os import listdir, system
from os.path import isfile, isdir, join

from PyQt4 import QtCore, QtGui

from metafileWidget import Ui_MetafileWidget
from utils import mime
from utils import hachoir_meta, gnome_meta, gio_meta


class AppButton(QtGui.QPushButton):
	def __init__(self, parent=None, appDB=False):
		"""
		Push Buttons for opening selected file in suggested app
		"""
		super(AppButton, self).__init__(parent)
		self.appDB = appDB
		QtCore.QMetaObject.connectSlotsByName(self)
	
	def mousePressEvent(self, event):
		key = unicode(self.text())
		if self.appDB.has_key(key):
			system('%s %s' % (self.appDB[key], self.appDB['URL']))
		

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
		
		# apps for a file DB
		self.appDB = {'URL': url}
		
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
		index = self.ui.metaInfo.addItem(textWidget, 'File Info')
		self.ui.metaInfo.setCurrentIndex(index)
		
		meta = gnome_meta.get_meta_info(url)
		app_name = False
		if meta and len(meta) > 0:
			gnomeLayout = QtGui.QVBoxLayout()
			
			description = QtGui.QLabel('<b>%s</b>' % meta['description'].decode('utf-8'))
			description.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
			gnomeLayout.addWidget(description)
			
			metaText = meta['mime'].replace('/', '\n')
			mimeLabel = QtGui.QLabel(metaText)
			mimeLabel.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
			gnomeLayout.addWidget(mimeLabel)
			
			if meta['default_app'] and len(meta['default_app']) > 0:
				app = AppButton(appDB = self.appDB)
				app.setText(meta['default_app'][1].decode('utf-8'))
				i = mime.get_icon(meta['default_app'][0])
				if i:
					app.setIcon(QtGui.QIcon(i))
				
				app_name = meta['default_app'][1]
				#app_desktop = meta['default_app'][0]
				#app_bin = meta['default_app'][2]
				self.appDB[meta['default_app'][1].decode('utf-8')] = meta['default_app'][2]
				gnomeLayout.addWidget(app)
			
			if meta['other_apps'] and len(meta['other_apps']) > 1:
				for application in meta['other_apps']:
					app = AppButton(appDB = self.appDB)
					app.setText(application[1].decode('utf-8'))
					i = mime.get_icon(application[0])
					if i:
						app.setIcon(QtGui.QIcon(i))
					
					self.appDB[application[1].decode('utf-8')] = application[2]
					#app_desktop = application[0]
					#app_bin = application[2]
					gnomeLayout.addWidget(app)
			
			# add the layout with widgets to a frame
			gnomeLayout.addItem(QtGui.QSpacerItem(20, 209, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding))
			frame = QtGui.QFrame()
			frame.setLayout(gnomeLayout)
			
			index  = self.ui.metaInfo.addItem(frame, 'GNOME')
			if no_meta or app_name:
				self.ui.metaInfo.setCurrentIndex(index)
		
		meta = gio_meta.get_meta_info(url)
		if meta and len(meta) > 0:
			gioLayout = QtGui.QVBoxLayout()
			for application in meta:
				app = AppButton(appDB = self.appDB)
				app.setText(application['name'].decode('utf-8'))
				app.setToolTip(application['description'].decode('utf-8'))
				i = mime.get_icon_by_exec(application['exec'])
				if i:
					app.setIcon(QtGui.QIcon(i))
				
				self.appDB[application['name'].decode('utf-8')] = application['exec']
				gioLayout.addWidget(app)
				#if app['description']:
					#text += u'<b>Description</b>: %s<br />' % app['description'].decode('utf-8')
				#text += u'<b>Executable</b>: %s<br /><br />' % app['exec']
			
			gioLayout.addItem(QtGui.QSpacerItem(20, 209, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding))
			frame = QtGui.QFrame()
			frame.setLayout(gioLayout)
			
			index  = self.ui.metaInfo.addItem(frame, 'GNOME / GIO')
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
	
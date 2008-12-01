# -*- coding: utf-8 -*-
import codecs
from os import listdir
from os.path import isfile, isdir, expanduser, join

from PyQt4 import QtCore, QtGui, Qsci

from fileWidget import Ui_FileWidget
from utils import mime

class fileWidget(QtGui.QWidget):
	def __init__(self, parent=None, url=False, mainWindow=False, newTab=False):
		super(fileWidget, self).__init__(parent)
		self.ui = Ui_FileWidget()
		self.ui.setupUi(self)
		# kill the margin between widgets
		l = self.layout()
		l.setMargin(0)
		# set the lineEdit-URL to be as high as buttons
		self.ui.url.setSizePolicy(QtGui.QSizePolicy.MinimumExpanding,QtGui.QSizePolicy.Preferred)
		# set the first box of navigation menu to get maximum size (that one with lineEdit-URL)
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
		
		# get mime so code highlighting can be set
		# set other QSCintilla settings
		mimetype = unicode(mime.get_mime(url))
		ext = url.split('.')[-1]
		font = QtGui.QFont()
		font.setFamily("Verdana")
		font.setFixedPitch(True)
		font.setPointSize(10)
		fm = QtGui.QFontMetrics(font)
		self.ui.editor.setUtf8(True)
		self.ui.editor.setMarginWidth(0, fm.width( "00000" ) + 5)
		self.ui.editor.setMarginLineNumbers(0, True)
		self.ui.editor.setBraceMatching(Qsci.QsciScintilla.SloppyBraceMatch)
		
		print mimetype

		if mimetype:
			if mimetype == 'application/x-csh' or mimetype == 'application/x-sh' or mimetype == 'text/x-script.zsh' or mimetype == 'application/x-shellscript':
				lexer = Qsci.QsciLexerBash()
				self.ui.editor.setLexer(lexer)
			elif mimetype == 'text/x-csrc' or mimetype == 'text/x-chdr' or ext == 'h' or mimetype == 'text/x-c' or mimetype == 'text/x-c++src':
				lexer = Qsci.QsciLexerCPP()
				self.ui.editor.setLexer(lexer)
			elif mimetype == 'text/css':
				lexer = Qsci.QsciLexerCSS()
				self.ui.editor.setLexer(lexer)
			elif mimetype == 'text/x-csharp':
				lexer = Qsci.QsciLexerCSharp()
				self.ui.editor.setLexer(lexer)
			elif mimetype == 'text/x-dsrc':
				lexer = Qsci.QsciLexerD()
				self.ui.editor.setLexer(lexer)
			elif mimetype == 'text/x-cmake':
				lexer = Qsci.QsciLexerCMake()
				self.ui.editor.setLexer(lexer)
			elif mimetype == 'text/x-makefile':
				lexer = Qsci.QsciLexerMakefile()
				self.ui.editor.setLexer(lexer)
			elif mimetype == 'text/x-patch':
				lexer = Qsci.QsciLexerDiff()
				self.ui.editor.setLexer(lexer)
			elif mimetype == 'text/x-fortran':
				lexer = Qsci.QsciLexerFortran()
				self.ui.editor.setLexer(lexer)
			elif mimetype == 'text/html':
				lexer = Qsci.QsciLexerHTML()
				self.ui.editor.setLexer(lexer)
			elif mimetype == 'text/x-java':
				lexer = Qsci.QsciLexerJava()
				self.ui.editor.setLexer(lexer)
			elif mimetype == 'application/javascript':
				lexer = Qsci.QsciLexerJavaScript()
				self.ui.editor.setLexer(lexer)
			elif mimetype == 'application/x-perl':
				lexer = Qsci.QsciLexerPerl()
				self.ui.editor.setLexer(lexer)
			elif mimetype == 'text/x-python':
				lexer = Qsci.QsciLexerPython()
				self.ui.editor.setLexer(lexer)
			elif mimetype == 'application/x-php':
				lexer = Qsci.QsciLexerHTML()
				self.ui.editor.setLexer(lexer)
			elif mimetype == 'application/x-ruby':
				lexer = Qsci.QsciLexerRuby()
				self.ui.editor.setLexer(lexer)
			elif mimetype == 'text/x-sql':
				lexer = Qsci.QsciLexerSQL()
				self.ui.editor.setLexer(lexer)
			elif mimetype == 'text/x-tcl':
				lexer = Qsci.QsciLexerTCL()
				self.ui.editor.setLexer(lexer)
			elif mimetype == 'application/xml':
				lexer = Qsci.QsciLexerXML()
				self.ui.editor.setLexer(lexer)
			elif ext == 'yml':
				lexer = Qsci.QsciLexerYAML()
				self.ui.editor.setLexer(lexer)
		
		"""
		ToDo:
			- Improve / FIX THIS
		"""
		try:
			text = codecs.open(url,'rw','utf-8').read()
		except:
			text = open(url).read()

		self.ui.editor.setText(text)
		
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
	
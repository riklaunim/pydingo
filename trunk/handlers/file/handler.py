# -*- coding: utf-8 -*-
import codecs
from os import listdir
from os.path import isfile, isdir, expanduser, join

from PyQt4 import QtCore, QtGui, Qsci

from fileWidget import Ui_FileWidget

class fileWidget(QtGui.QWidget):
	def __init__(self, parent=None, url=False, mainWindow=False, newTab=False, mime=False):
		super(fileWidget, self).__init__(mainWindow.main)
		self.ui = Ui_FileWidget()
		self.ui.setupUi(self)
		# kill the margin between widgets
		l = self.layout()
		l.setMargin(0)
		# set the lineEdit-URL to be as high as buttons
		self.ui.url.setSizePolicy(QtGui.QSizePolicy.MinimumExpanding,QtGui.QSizePolicy.Preferred)
		# set the first box of navigation menu to get maximum size (that one with lineEdit-URL)
		self.ui.splitter.setStretchFactor(0,1)
		
		self.parent = mainWindow.main
		self.mainWindow = mainWindow
		
		if not url:
			url = self.ui.url.text()
		self.url = url
		
		# use filename for tab name
		tabName = url.split('/')
		tabName = tabName[-1]
		
		# set the URL
		self.ui.url.setText(url)
		
		# get mime so code highlighting can be set
		# set other QSCintilla settings
		if mime:
			mimetype = unicode(mime)
		else:
			raise IOError, 'No mime for %s' % tabName
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
			elif mimetype == 'application/javascript' or mimetype == 'application/x-javascript':
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
			index = self.parent.addTab(self, tabName)
			self.parent.setCurrentIndex(index)
		else:
			index = self.parent.currentIndex()
			self.parent.removeTab(index)
			self.parent.insertTab(index, self, tabName)
			self.parent.setCurrentIndex(index)
		
		
		QtCore.QObject.connect(self.ui.editor,QtCore.SIGNAL("textChanged()"), self.file_modified)
		QtCore.QObject.connect(self.ui.save,QtCore.SIGNAL("clicked()"), self.file_save)
		QtCore.QObject.connect(self.ui.saveas,QtCore.SIGNAL("clicked()"), self.file_saveAs)
		QtCore.QObject.connect(self.ui.undo,QtCore.SIGNAL("clicked()"), self.file_undo)
		QtCore.QObject.connect(self.ui.redo,QtCore.SIGNAL("clicked()"), self.file_redo)
		QtCore.QObject.connect(self.ui.find,QtCore.SIGNAL("clicked()"), self.file_find)
		
		QtCore.QObject.connect(self.ui.newTab,QtCore.SIGNAL("clicked()"), self.mainWindow.new_tab)
		QtCore.QObject.connect(self.ui.back,QtCore.SIGNAL("clicked()"), self.back)
		QtCore.QObject.connect(self.ui.next,QtCore.SIGNAL("clicked()"), self.next)
		QtCore.QObject.connect(self.ui.close,QtCore.SIGNAL("clicked()"), self.close_tab)
		QtCore.QObject.connect(self.ui.up,QtCore.SIGNAL("clicked()"), self.up_clicked)
		QtCore.QObject.connect(self.ui.home,QtCore.SIGNAL("clicked()"), self.home)
		QtCore.QObject.connect(self.ui.url,QtCore.SIGNAL("returnPressed()"), self.url_handler)
		QtCore.QMetaObject.connectSlotsByName(self)
	
	def file_find(self):
		"""
		Find icon clicked
		* ToDo: add menu here for find, find/replace, find next
		"""
		if not self.ui.editor.findNext():
			response = QtGui.QInputDialog.getText(self, 'Find', 'Find:', QtGui.QLineEdit.Normal)
			if response[1] and len(response[0]) > 0:
				self.ui.editor.findFirst(response[0], False, False, False, False)
	
	def file_modified(self):
		"""
		File text in the editor changed
		* enable save button
		* check if undo/redo button can be activated and do it
		"""
		self.ui.save.setEnabled(True)
		
		if self.ui.editor.isRedoAvailable():
			self.ui.redo.setEnabled(True)
		else:
			self.ui.redo.setEnabled(False)
		
		if self.ui.editor.isUndoAvailable():
			self.ui.undo.setEnabled(True)
		else:
			self.ui.undo.setEnabled(False)
	
	def file_undo(self):
		"""
		Undo button clicked
		* undo one action
		* check if there are undos/redos available etc
		"""
		self.ui.editor.undo()
		
		if self.ui.editor.isRedoAvailable():
			self.ui.redo.setEnabled(True)
		else:
			self.ui.redo.setEnabled(False)
		
		if self.ui.editor.isUndoAvailable():
			self.ui.undo.setEnabled(True)
		else:
			self.ui.undo.setEnabled(False)
		
		if self.ui.editor.isModified():
			self.ui.save.setEnabled(True)
		else:
			self.ui.save.setEnabled(False)
	
	def file_redo(self):
		"""
		Redi button clicked
		* redo one action
		* check if there are undos/redos available etc
		"""
		self.ui.editor.redo()
		
		if self.ui.editor.isRedoAvailable():
			self.ui.redo.setEnabled(True)
		else:
			self.ui.redo.setEnabled(False)
		
		if self.ui.editor.isUndoAvailable():
			self.ui.undo.setEnabled(True)
		else:
			self.ui.undo.setEnabled(False)
		
		if self.ui.editor.isModified():
			self.ui.save.setEnabled(True)
		else:
			self.ui.save.setEnabled(False)
	
	def file_save(self):
		"""
		save button clicked, save the changes
		"""
		text = self.ui.editor.text()
		handle = open(self.url, 'w')
		handle.write(text)
		handle.close()
		self.ui.save.setEnabled(False)
		self.ui.editor.setModified(False)
	
	def file_saveAs(self):
		"""
		Save As button clicked
		* show file dialog and enable saving under different name
		"""
		fd = QtGui.QFileDialog(self)
		newfile = fd.getSaveFileName()
		if newfile:
			s = open(newfile,'w')
			s.write(self.ui.editor.text())
			s.close()
			
			self.ui.save.setEnabled(False)
			self.ui.editor.setModified(False)
			
			## new file, remove old and add the new one to the watcher
			#if self.filename and str(newfile) != str(self.filename):
				#self.watcher.removePath(self.filename)
				#self.watcher.addPath(newfile)
				#self.filename = newfile
	
	####################
	def back(self):
		"""
		Extend the Back button click to handle not saved modified files
		"""
		if self.ui.editor.isModified():
			SAVE = 'Save And Go'
			DISCARD = 'Discard Changes'
			CANCEL = 'Cancel'
			
			message = QtGui.QMessageBox(self)
			message.setText('Changes haven\'t been saved')
			message.setWindowTitle('PyDingo Text Editor')
			message.setIcon(QtGui.QMessageBox.Question)
			message.addButton(SAVE, QtGui.QMessageBox.AcceptRole)
			message.addButton(DISCARD, QtGui.QMessageBox.DestructiveRole)
			message.addButton(CANCEL, QtGui.QMessageBox.RejectRole)
			message.setDetailedText('Unsaved changes in: ' + self.ui.url.text())
			message.exec_()
			response = message.clickedButton().text()
			if response == DISCARD:
				self.mainWindow.back()
			elif response == SAVE:
				self.file_save()
				self.mainWindow.back()
		else:
			self.mainWindow.back()
	
	def next(self):
		"""
		Extend the Next button click to handle not saved modified files
		"""
		if self.ui.editor.isModified():
			SAVE = 'Save And Go'
			DISCARD = 'Discard Changes'
			CANCEL = 'Cancel'
			
			message = QtGui.QMessageBox(self)
			message.setText('Changes haven\'t been saved')
			message.setWindowTitle('PyDingo Text Editor')
			message.setIcon(QtGui.QMessageBox.Question)
			message.addButton(SAVE, QtGui.QMessageBox.AcceptRole)
			message.addButton(DISCARD, QtGui.QMessageBox.DestructiveRole)
			message.addButton(CANCEL, QtGui.QMessageBox.RejectRole)
			message.setDetailedText('Unsaved changes in: ' + self.ui.url.text())
			message.exec_()
			response = message.clickedButton().text()
			if response == DISCARD:
				self.mainWindow.next()
			elif response == SAVE:
				self.file_save()
				self.mainWindow.next()
		else:
			self.mainWindow.next()
	
	def close_tab(self):
		"""
		Extend the Close Tab button click to handle not saved modified files
		"""
		if self.ui.editor.isModified():
			SAVE = 'Save And Go'
			DISCARD = 'Discard Changes'
			CANCEL = 'Cancel'
			
			message = QtGui.QMessageBox(self)
			message.setText('Changes haven\'t been saved')
			message.setWindowTitle('PyDingo Text Editor')
			message.setIcon(QtGui.QMessageBox.Question)
			message.addButton(SAVE, QtGui.QMessageBox.AcceptRole)
			message.addButton(DISCARD, QtGui.QMessageBox.DestructiveRole)
			message.addButton(CANCEL, QtGui.QMessageBox.RejectRole)
			message.setDetailedText('Unsaved changes in: ' + self.ui.url.text())
			message.exec_()
			response = message.clickedButton().text()
			if response == DISCARD:
				self.mainWindow.close_tab()
			elif response == SAVE:
				self.file_save()
				self.mainWindow.close_tab()
		else:
			self.mainWindow.close_tab()
	
	def up_clicked(self):
		"""
		Extend the UP button click to handle not saved modified files
		"""
		if self.ui.editor.isModified():
			SAVE = 'Save And Go'
			DISCARD = 'Discard Changes'
			CANCEL = 'Cancel'
			
			message = QtGui.QMessageBox(self)
			message.setText('Changes haven\'t been saved')
			message.setWindowTitle('PyDingo Text Editor')
			message.setIcon(QtGui.QMessageBox.Question)
			message.addButton(SAVE, QtGui.QMessageBox.AcceptRole)
			message.addButton(DISCARD, QtGui.QMessageBox.DestructiveRole)
			message.addButton(CANCEL, QtGui.QMessageBox.RejectRole)
			message.setDetailedText('Unsaved changes in: ' + self.ui.url.text())
			message.exec_()
			response = message.clickedButton().text()
			if response == DISCARD:
				self.mainWindow.up_clicked()
			elif response == SAVE:
				self.file_save()
				self.mainWindow.up_clicked()
		else:
			self.mainWindow.up_clicked()
	
	def url_handler(self):
		"""
		Extend the URL change to handle not saved modified files
		"""
		if self.ui.editor.isModified():
			SAVE = 'Save And Go'
			DISCARD = 'Discard Changes'
			CANCEL = 'Cancel'
			
			message = QtGui.QMessageBox(self)
			message.setText('Changes haven\'t been saved')
			message.setWindowTitle('PyDingo Text Editor')
			message.setIcon(QtGui.QMessageBox.Question)
			message.addButton(SAVE, QtGui.QMessageBox.AcceptRole)
			message.addButton(DISCARD, QtGui.QMessageBox.DestructiveRole)
			message.addButton(CANCEL, QtGui.QMessageBox.RejectRole)
			message.setDetailedText('Unsaved changes in: ' + self.url)
			message.exec_()
			response = message.clickedButton().text()
			if response == DISCARD:
				self.mainWindow.url_handler()
			elif response == SAVE:
				self.file_save()
				self.mainWindow.url_handler()
		else:
			self.mainWindow.url_handler()
	
	def home(self):
		"""
		Extend the home button click to handle not saved modified files
		"""
		if self.ui.editor.isModified():
			SAVE = 'Save And Go'
			DISCARD = 'Discard Changes'
			CANCEL = 'Cancel'
			
			message = QtGui.QMessageBox(self)
			message.setText('Changes haven\'t been saved')
			message.setWindowTitle('PyDingo Text Editor')
			message.setIcon(QtGui.QMessageBox.Question)
			message.addButton(SAVE, QtGui.QMessageBox.AcceptRole)
			message.addButton(DISCARD, QtGui.QMessageBox.DestructiveRole)
			message.addButton(CANCEL, QtGui.QMessageBox.RejectRole)
			message.setDetailedText('Unsaved changes in: ' + self.ui.url.text())
			message.exec_()
			response = message.clickedButton().text()
			if response == DISCARD:
				self.mainWindow.home_clicked()
			elif response == SAVE:
				self.file_save()
				self.mainWindow.home_clicked()
		else:
			self.mainWindow.home_clicked()
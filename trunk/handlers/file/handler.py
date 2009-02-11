# -*- coding: utf-8 -*-
# Text editor based on QScintilla

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
		
		# monitor file for changes
		self.watcher = QtCore.QFileSystemWatcher(self)
		
		if not url:
			url = self.ui.url.text()
		self.url = url
		 
		if not self.url:
			# new file, does not exist
			tabName = 'New File'
			self.newFile = True
			mimetype = False
		else:
			self.newFile = False
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
		self.ui.editor.setFolding(Qsci.QsciScintilla.BoxedTreeFoldStyle)
		self.ui.editor.setAutoIndent(True)
		
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
		
		if not self.newFile:
			"""
			ToDo:
				- Improve / FIX THIS
			"""
			try:
				text = codecs.open(url,'rw','utf-8').read()
			except:
				text = open(url).read()
	
			# load file text
			self.ui.editor.setText(text)
			# set file watcher:
			self.watcher.addPath(self.url)
			self.ui.editor.setModified(False)
		
		# set the tab
		if newTab:
			index = self.parent.addTab(self, tabName)
			self.parent.setCurrentIndex(index)
		else:
			index = self.parent.currentIndex()
			self.parent.removeTab(index)
			self.parent.insertTab(index, self, tabName)
			self.parent.setCurrentIndex(index)
		
		# Key shortcuts
		find = QtGui.QKeySequence(QtGui.QKeySequence.Find)
		self.ui.find.setShortcut(find)
		
		redo = QtGui.QKeySequence(QtGui.QKeySequence.Redo)
		self.ui.redo.setShortcut(redo)
		
		undo = QtGui.QKeySequence(QtGui.QKeySequence.Undo)
		self.ui.undo.setShortcut(undo)
		
		save = QtGui.QKeySequence(QtGui.QKeySequence.Save)
		self.ui.save.setShortcut(save)
		
		QtCore.QObject.connect(self.ui.editor,QtCore.SIGNAL("textChanged()"), self.file_modified)
		QtCore.QObject.connect(self.ui.save,QtCore.SIGNAL("clicked()"), self.file_save)
		QtCore.QObject.connect(self.ui.saveas,QtCore.SIGNAL("clicked()"), self.file_saveAs)
		QtCore.QObject.connect(self.ui.undo,QtCore.SIGNAL("clicked()"), self.file_undo)
		QtCore.QObject.connect(self.ui.redo,QtCore.SIGNAL("clicked()"), self.file_redo)
		QtCore.QObject.connect(self.ui.find,QtCore.SIGNAL("clicked()"), self.file_find)
		# detect external changes to open file
		QtCore.QObject.connect(self.watcher,QtCore.SIGNAL("fileChanged(const QString&)"), self.file_changed)
		
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
		if self.ui.editor.hasSelectedText():
			response = QtGui.QInputDialog.getText(self, 'Find', 'Find:', QtGui.QLineEdit.Normal, self.ui.editor.selectedText())
		else:
			response = QtGui.QInputDialog.getText(self, 'Find', 'Find:', QtGui.QLineEdit.Normal)
		if response[1] and len(response[0]) > 0:
			if not self.ui.editor.findFirst(response[0], False, False, False, False):
				msg = QtGui.QMessageBox('Find', 'Cannot find "%s"' % response[0], QtGui.QMessageBox.Information, QtGui.QMessageBox.AcceptRole, QtGui.QMessageBox.NoButton, QtGui.QMessageBox.NoButton)
				msg.exec_()
	
	def file_changed(self, path):
		response = False
		# disable watcher and modification state of the file so this wont call itself
		self.watcher.removePath(self.url)
		self.ui.editor.setModified(False)
		# buttons texts
		SAVE = 'Save As'
		RELOAD = 'Reload File'
		CANCEL = 'Cancel'
		message = QtGui.QMessageBox(self)
		message.setIcon(QtGui.QMessageBox.Warning)
		message.setText('The document has been modified or deleted.')
		message.setInformativeText("Do you want to save your changes?")
		message.setWindowTitle('PyDingo Text Editor')
		message.setIcon(QtGui.QMessageBox.Warning)
		message.addButton(SAVE, QtGui.QMessageBox.AcceptRole)
		message.addButton(RELOAD, QtGui.QMessageBox.DestructiveRole)
		message.addButton(CANCEL, QtGui.QMessageBox.RejectRole)
		message.setDetailedText('The file "' + str(path) + '" have been changed or removed by other application. What do you want to do ?')
		message.exec_()
		response = message.clickedButton().text()
		# save current file under a new or old name
		if response == SAVE:
			fd = QtGui.QFileDialog(self)
			newfile = fd.getSaveFileName()
			if newfile:
				s = open(newfile,'w')
				s.write(self.ui.editor.text())
				s.close()
				self.mainWindow.url_handler(url=newfile)
		# reload the text in the editor
		elif response == RELOAD:
			self.mainWindow.url_handler()
		else:
			# add watcher (Cancel pressed)
			self.watcher.addPath(self.url)
	
	def file_modified(self):
		"""
		File text in the editor changed
		* enable save button
		* check if undo/redo button can be activated and do it
		"""
		if not self.newFile:
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
			if not self.newFile:
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
			if not self.newFile:
				self.ui.save.setEnabled(True)
		else:
			self.ui.save.setEnabled(False)
	
	def file_saveAs(self):
		"""
		Save As button clicked
		* show file dialog and enable saving under different name
		"""
		self.watcher.removePath(self.url)
		fd = QtGui.QFileDialog(self)
		newfile = fd.getSaveFileName()
		if newfile:
			s = open(newfile,'w')
			s.write(self.ui.editor.text())
			s.close()
			
			self.ui.save.setEnabled(False)
			self.ui.url.setText(newfile)
			if not self.newFile:
				self.watcher.addPath(newfile)
			else:
				self.mainWindow.url_handler(url=newfile)
				
			self.ui.editor.setModified(False)
			
			## new file, remove old and add the new one to the watcher
			#if self.filename and str(newfile) != str(self.filename):
				#self.watcher.removePath(self.filename)
				#self.watcher.addPath(newfile)
				#self.filename = newfile
	
	def file_save(self):
		"""
		save button clicked, save the changes
		"""
		# backup
		if self.newFile:
			return self.file_saveAs()
		backup = open(self.url, 'r').read()
		handle = open('%s~' % self.url, 'w')
		handle.write(backup)
		handle.close()
		
		self.watcher.removePath(self.url)
		text = self.ui.editor.text()
		handle = open(self.url, 'w')
		handle.write(text)
		handle.close()
		self.watcher.addPath(self.url)
		self.ui.save.setEnabled(False)
		self.ui.editor.setModified(False)
	
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
			message.setInformativeText("Do you want to save your changes?")
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
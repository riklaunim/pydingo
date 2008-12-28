# -*- coding: utf-8 -*-
# Custom QDirModel with reimplemented few methods

from sys import exc_info
from traceback import format_exception
from os.path import isfile, isdir, join
import shutil

from PyQt4 import QtCore, QtGui

class FileManagerModel(QtGui.QDirModel):
	def __init__(self, parent=None):
		"""
		Custom QDirModel with Drag & Drop support
		"""
		self.parent = parent
		super(FileManagerModel, self).__init__(parent)
	
	def flags(self, index):
		"""
		Enable drops of elements on folders (readOnly is True)
		"""
		if index.isValid() and self.isDir(index):
			return QtCore.Qt.ItemIsDropEnabled | QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsDragEnabled
		else:
			return QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsDragEnabled
	
	def dropMimeData(self, data, action, row, column, parent):
		"""
		Dropping elements on folders
		"""
		currentDir = unicode(self.parent.ui.url.text())
		dst = join(currentDir, unicode(parent.data().toString()))
		items = data.urls()
		if len(items) > 0 and isdir(dst):
			MOVE = 'Move'
			COPY = 'Copy'
			CANCEL = 'Cancel'
			itms = ''
			for i in items:
				itms += '- %s\n' % i.toLocalFile()
			
			message = QtGui.QMessageBox(self.parent)
			message.setText('What to do with selected items?')
			message.setWindowTitle('PyDingo File Manager')
			message.setIcon(QtGui.QMessageBox.Question)
			message.addButton(MOVE, QtGui.QMessageBox.AcceptRole)
			message.addButton(COPY, QtGui.QMessageBox.AcceptRole)
			message.addButton(CANCEL, QtGui.QMessageBox.RejectRole)
			message.setDetailedText(itms)
			message.exec_()
			response = message.clickedButton().text()
			
			if response == MOVE:
				for i in items:
					src = unicode(i.toLocalFile())
					if isdir(src):
						# If we move/copy a dir the destination must have it's name at the end
						qdir = QtCore.QDir(src)
						dst = join(dst, unicode(qdir.dirName()))
					else:
						dst = join(currentDir, unicode(parent.data().toString()))
					
					try:
						shutil.move(src, dst)
					except:
						exc = exc_info()
						exc = format_exception(exc[0], exc[1], exc[2])
						msg = QtGui.QMessageBox('Error when moving items', '<b>An error occured when moving files/folders</b>:<br>%s' % unicode(exc[-1]), QtGui.QMessageBox.Critical, QtGui.QMessageBox.AcceptRole, QtGui.QMessageBox.NoButton, QtGui.QMessageBox.NoButton)
						exc = ''.join(exc)
						msg.setDetailedText(unicode(exc))
						msg.exec_()
						return False
				self.parent.reload_items()
			
			if response == COPY:
				for i in items:
					src = unicode(i.toLocalFile())
					if isfile(src):
						dst = join(currentDir, unicode(parent.data().toString()))
						try:
							shutil.copy(src, dst)
						except:
							exc = exc_info()
							exc = format_exception(exc[0], exc[1], exc[2])
							msg = QtGui.QMessageBox('Error when copying files', '<b>An error occured when copying files</b>:<br>%s' % unicode(exc[-1]), QtGui.QMessageBox.Critical, QtGui.QMessageBox.AcceptRole, QtGui.QMessageBox.NoButton, QtGui.QMessageBox.NoButton)
							exc = ''.join(exc)
							msg.setDetailedText(unicode(exc))
							msg.exec_()
							return False
					else:
						# If we move/copy a dir the destination must have it's name at the end
						qdir = QtCore.QDir(src)
						dst = join(dst, unicode(qdir.dirName()))
						try:
							shutil.copytree(src, dst)
						except:
							exc = exc_info()
							exc = format_exception(exc[0], exc[1], exc[2])
							msg = QtGui.QMessageBox('Error when copying a folder', '<b>An error occured when copying a folder</b>:<br>%s' % unicode(exc[-1]), QtGui.QMessageBox.Critical, QtGui.QMessageBox.AcceptRole, QtGui.QMessageBox.NoButton, QtGui.QMessageBox.NoButton)
							exc = ''.join(exc)
							msg.setDetailedText(unicode(exc))
							msg.exec_()
							return False
			return True
		return False

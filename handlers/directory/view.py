# -*- coding: utf-8 -*-
# Custom QListView for the filemanager

from sys import exc_info
from traceback import format_exception
from os.path import isfile, isdir, join
import shutil

from PyQt4 import QtCore, QtGui

class FileManagerView(QtGui.QListView):
	def __init__(self, parent=None):
		"""
		Custom with handling keysequences like copy/cut/paste
		"""
		self.parent = parent
		super(FileManagerView, self).__init__(parent)
	def keyPressEvent(self, event):
		"""
		Handle Copy, Paste, Cut, Delete from keyboard shortcuts
		"""
		# modelindexes of selected items
		items = self.selectedIndexes()
		# the list to which we save the items
		container = self.parent.mainWindow.filemanagerContainer
		if len(items) > 0:
			"""
			Copy, Cut - save the list of items to a global container, Delete
			"""
			itm = []
			# we want nice paths to selected items, as modelindexes would be useless in another folder
			for i in items:
				itm.append(unicode(self.parent.model.filePath(i)))
			
			if event.matches(QtGui.QKeySequence.Copy):
				event.accept()
				print 'copy'
				# save items to the container
				self.parent.mainWindow.filemanagerContainer = itm
				self.parent.mainWindow.filemanagerContainerType = 'COPY'
			elif event.matches(QtGui.QKeySequence.Cut):
				event.accept()
				print 'cut'
				# save items to the container
				self.parent.mainWindow.filemanagerContainer = itm
				self.parent.mainWindow.filemanagerContainerType = 'MOVE'
			elif event.matches(QtGui.QKeySequence.Delete):
				event.accept()
				print 'delete-move-to-trash / NOT IMPLEMENTED'
			else:
				event.ignore()
		if len(container) > 0:
			"""
			Paste action - copy items from global container to current directory
			"""
			if event.matches(QtGui.QKeySequence.Paste):
				event.accept()
				print 'paste'
				# current folder is the destination folder
				parent = self.parent.ui.listView.rootIndex()
				dst = unicode(self.parent.model.filePath(parent))
				
				if self.parent.mainWindow.filemanagerContainerType == 'MOVE':
					for src in container:
						if isdir(src):
							#If we move/copy a dir the destination must have it's name at the end
							qdir = QtCore.QDir(src)
							dst = join(dst, unicode(qdir.dirName()))
						else:
							dst = unicode(self.parent.model.filePath(parent))
						
						try:
							shutil.move(src, dst)
						except:
							exc = exc_info()
							exc = format_exception(exc[0], exc[1], exc[2])
							msg = QtGui.QMessageBox('Error when moving items', '<b>An error occured when moving files/folders</b>:<br>%s' % unicode(exc[-1]), QtGui.QMessageBox.Critical, QtGui.QMessageBox.AcceptRole, QtGui.QMessageBox.NoButton, QtGui.QMessageBox.NoButton)
							exc = ''.join(exc)
							msg.setDetailedText(unicode(exc))
							msg.exec_()
					self.parent.reload_items()
				
				if self.parent.mainWindow.filemanagerContainerType == 'COPY':
					for src in container:
						if isfile(src):
							dst = unicode(self.parent.model.filePath(parent))
							try:
								shutil.copy(src, dst)
							except:
								exc = exc_info()
								exc = format_exception(exc[0], exc[1], exc[2])
								msg = QtGui.QMessageBox('Error when copying files', '<b>An error occured when copying files</b>:<br>%s' % unicode(exc[-1]), QtGui.QMessageBox.Critical, QtGui.QMessageBox.AcceptRole, QtGui.QMessageBox.NoButton, QtGui.QMessageBox.NoButton)
								exc = ''.join(exc)
								msg.setDetailedText(unicode(exc))
								msg.exec_()
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
					self.parent.reload_items()
			else:
				event.ignore()
		else:
			event.ignore()

# -*- coding: utf-8 -*-
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
		items = self.selectedIndexes()
		container = self.parent.mainWindow.filemanagerContainer
		if len(items) > 0:
			"""
			Copy, Cut - save the list of items to a global container, Delete
			"""
			if event.matches(QtGui.QKeySequence.Copy):
				event.accept()
				# save items to the container
				self.parent.mainWindow.filemanagerContainer = items
			elif event.matches(QtGui.QKeySequence.Cut):
				event.accept()
				# save items to the container
				self.parent.mainWindow.filemanagerContainer = items
			elif event.matches(QtGui.QKeySequence.Delete):
				event.accept()
				print 'delete'
			else:
				event.ignore()
		elif len(container) > 0:
			"""
			Paste action - copy items from global container to current directory
			"""
			if event.matches(QtGui.QKeySequence.Paste):
				event.accept()
				print 'paste'
			else:
				event.ignore()
		else:
			event.ignore()
		print self.parent.mainWindow.filemanagerContainer
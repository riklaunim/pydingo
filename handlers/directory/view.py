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
		if event.matches(QtGui.QKeySequence.Copy):
			event.accept()
			print 'copy'
		elif event.matches(QtGui.QKeySequence.Cut):
			event.accept()
			print 'cut'
		elif event.matches(QtGui.QKeySequence.Paste):
			event.accept()
			print 'paste'
		elif event.matches(QtGui.QKeySequence.Delete):
			event.accept()
			print 'delete'
		else:
			event.ignore()
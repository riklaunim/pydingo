# -*- coding: utf-8 -*-
# Extraction of file metadata using cross platform Hachoir library

try:
	from hachoir_core.error import HachoirError
	from hachoir_core.cmd_line import unicodeFilename
	from hachoir_parser import createParser
	from hachoir_core.tools import makePrintable
	from hachoir_metadata import extractMetadata
	from hachoir_core.i18n import getTerminalCharset
except:
	print '*Optional dependency missing* No hachoir packages, meta information for binary files disabled'

def get_meta_info(filename):
	try:
		parser = createParser(filename, filename)
	except:
		return False
	if parser:
		try:
			metadata = extractMetadata(parser)
		except HachoirError, err:
			return False
		else:
			if metadata:
				return metadata.exportPlaintext()
	return False
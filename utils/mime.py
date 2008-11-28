import xdg.Mime

def get_mime(file):
	"""
	Return mime type of a file
	"""
	try:
		mime = xdg.Mime.get_type(unicode(file))
	except:
		return False
	return mime

def is_plaintext(mimetype):
	"""
	Check if mime is handled by QScintilla / is plaintext
	"""
	plain_mimes = ['application/javascript', 'application/xml', 'application/x-csh', 'application/x-sh', 'application/x-shellscript',
		'application/javascript', 'application/x-perl', 'application/x-php', 'application/x-ruby']
	
	if mimetype.startswith('text') or plain_mimes.count(mimetype) > 0:
		return True
	else:
		return False
	
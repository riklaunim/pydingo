import mimetypes

try:
	import xdg.Mime
except:
	xdg = False
	print '*Optional dependency missing* No pyxdg package. Please install it for unix/linux for better mime handling'

def get_mime(file):
	"""
	Return mime type of a file
	"""
	# xdg returns text/plain for everything on Windows :)
	if unicode(xdg.Mime.get_type('file.sql')) == u'text/x-sql':
		file = unicode(file)
		#try pyxdg linux/unix backed
		try:
			mime = xdg.Mime.get_type(file, name_pri=0)
		except:
			mime = False
	else:
		# fallback to python mimetypes module (on Windows)
		mimetypes.init()
		ext = u'.%s' % file.split('.')[-1]
		try:
			mime = mimetypes.types_map[ext]
		except:
			mime = False
	return mime

def is_plaintext(mimetype):
	"""
	Check if mime is plaintext
	"""
	# non text/* mimetypes that are used for text files
	plain_mimes = ['application/javascript', 'application/x-javascript', 'application/xml', 'application/x-csh', 'application/x-sh', 'application/x-shellscript',
		'application/javascript', 'application/x-perl', 'application/x-php', 'application/x-ruby']

	mimetype = unicode(mimetype)
	if plain_mimes.count(mimetype) > 0:
		return True
	elif mimetype.startswith('text'):
		return True
	
	return False
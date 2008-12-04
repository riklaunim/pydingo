import mimetypes

try:
	import xdg.Mime
except:
	xdg = False
	print '*Optional dependency missing* No pyxdg package. Please install it for unix/linux for better mime handling'

try:
	import gnomevfs
except:
	gnomevfs = False
	print '*Optional dependency missing* No gnome-vfs-python package. Install it if you use GNOME or related WM for application suggesting and mime detection'

from utils import hachoir_meta

def get_mime(file):
	"""
	Return mime type of a file
	"""
	file = unicode(file)
	mime = []
	
	#try pyxdg linux/unix backed
	try:
		xmime = xdg.Mime.get_type(file)
	except:
		pass
	else:
		mime.append(unicode(xmime))
		print 'xdg mime: %s' % xmime
	
	try:
		hmeta = hachoir_meta.get_meta_info(file)
	except:
		pass
	else:
		if hmeta and len(hmeta) > 0:
			for line in hmeta:
				if line.startswith('- MIME type: '):
					hmime = line.replace('- MIME type: ', '')
					mime.append(unicode(hmime))
					print 'hachoir mime: %s' % hmime
	
	# GNOME
	if gnomevfs:
		try:
			gmime = gnomevfs.get_mime_type(file)
		except:
			pass
		else:
			mime.append(unicode(gmime))
			print 'GNOME mime: %s' % gmime
	
	# fallback python mimetypes module (on Windows)
	mimetypes.init()
	ext = u'.%s' % file.split('.')[-1]
	try:
		mimes = mimetypes.types_map[ext]
	except:
		mimes = False
	else:
		print 'Mimetypes mime: %s' % mimes
		mime.append(unicode(mimes))
	
	print
	return mime

def is_plaintext(mimes):
	"""
	Check if mime is plaintext
	"""
	# non text/* mimetypes that are used for text files
	plain_mimes = ['application/javascript', 'application/x-javascript', 'application/xml', 'application/x-csh', 'application/x-sh', 'application/x-shellscript',
		'application/javascript', 'application/x-perl', 'application/x-php', 'application/x-ruby']
	
	if len(mimes) < 0:
		return False
	
	if plain_mimes.count(mimes[0]) > 0:
		return True
	elif not xdg and mimes[0].startswith('text'):
		# pyxdg on Windows returns text/plain to everything
		return True
	elif xdg and len(mimes) > 1 and mimes[0].startswith('text') and mimes[1].startswith('text'):
		return True
	else:
		return False
	
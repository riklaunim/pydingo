from os import listdir

from utils import mime

files = listdir('tests/files/')
for f in files:
	print '%s: %s' % (f, unicode(mime.get_mime('tests/files/%s' + f)))
from os import listdir

from utils import mime

files = listdir('tests/files/')
for f in files:
	print 'FILE: %s: %s' % (f, mime.get_mime('tests/files/%s' % f))
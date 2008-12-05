from os import listdir

from utils import mime

ROOT = '/home/piotr/svn/pydingo'

files = listdir('tests/files/')
for f in files:
	print 'FILE: %s:' % f
	mime.get_mime('%s/tests/files/%s' % (ROOT, f))
from distutils.core import setup
import py2exe

setup(windows=[{"script" : "run.py"}], options={"py2exe" : {"includes" : ["sip", "PyQt4", "PyQt4.QtNetwork"]}}) 
#python setup.py py2exe
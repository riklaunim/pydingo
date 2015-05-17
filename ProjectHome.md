PyDingo will be a cross-platform File Manager based on PyQt4. The key feature will be pluggable widgets that will handle various URLs (text editor for text files, file browser for folders, media player for multimedia files and so on) shown in tabs (or opening files in external applications assigned to such files). Tabs will be detachable as QDock external windows or embedded on the PyDingo window sides (thus allowing 2 panel or more file management).



The purpose of creating such application is to:

1. Learn more about PyQt4 :)

2. Create some solutions for common GUI application creation problems (there are web frameworks, but no GUI frameworks except Dabo or Tryton)

2a. Create articles about used Python modules, implemented features

3. Show that Python and PyQt4 can be used to create nice applications.


---

### Screenshots ###

+  [Linux](http://www.python.rk.edu.pl/site_media/resources/python.rk.edu.pl/images/pydinlin.png)

+  [Mac OS X](http://www.python.rk.edu.pl/site_media/resources/python.rk.edu.pl/images/pydinmac.png)

+  [Windows XP](http://www.python.rk.edu.pl/site_media/resources/python.rk.edu.pl/images/pydinwin.png)

+ [Scintilla based text editor](http://www.python.rk.edu.pl/site_media/resources/python.rk.edu.pl/images/pydingo2.png)

+ [Native look in GNOME](http://www.python.rk.edu.pl/site_media/resources/python.rk.edu.pl/images/pydingo_gnome.png)



---


### Contact, comments, help, other ###
**riklaunim@gmail.com (mail/GTalk/jabber)**


---


### Code checkout ###
The code is in the SVN repository:
```
svn checkout http://pydingo.googlecode.com/svn/trunk/ pydingo
```
To run the application use:
```
python run.py
```
You will need PyQt4, qscintilla-python, [pyxdg](http://pyxdg.freedesktop.org/), and optionally other modules in the future. Should run on Windows/Mac OS X/Linux/Unix where PyQt4 is available. pyxdg as a mime backed will be changed in near future (other utilities needed for Windows, and  OS X).


---

# Alpha 0.39 release #
This sub-release contains some fixes, code improvements over 0.3, but still lacks some new functionality planned for 0.4 release (settings, docking, and detaching). Source code:
**http://pydingo.googlecode.com/files/pydingo-0.39.zip**

# Alpha 0.3 release #
If you want to test whats going on in the project use the SVN code. 0.3 is getting old, however you can test windows binary - if it works and has all the DLL (report bugs). 0.3 release offers:
```
* Basic File browsing
* Text files editor
* Meta/Mime data preview for binary files with ability to run in suggested app (Linux/Unix currently)
* Basic web browser (WebKit)
```
**Dependencies**: PyQt4 (Qt 4.4 or newer), qscintilla-python, pyxdg (Linux/Unix, highly recommended), hachoir (optional, recommended), gnome-vfs-python (optional, GNOME/Other application suggesting for files) and / or newer pygobject with GIO bindings (optional, GNOME/Other application suggesting for files)

**OS**: Linux, Windows tested. Should work on OS X and other Unix systems.

**Source**: http://pydingo.googlecode.com/files/pydingo-src-0.3.zip

**Windows binary**: http://pydingo.googlecode.com/files/pydingo-win32-0.3.zip (extract and click on "run.exe")



# Alpha stage road map #

### Stage 4 - In Progress ###
#### 0.4 release after completion ####
```
* Functional file management
* Fully cross-platform and reusable libraries for file MIME/Meta handling, application suggestion
* Tray icon / notifications
* Try to add better support for MS Windows and Mac OS X:
	* binary builds
* Create terminal widget-handler (qtermwidget or class used in Eric)
* Detachable tabs
@ Update widget-handlers tutorials

@ Write full documentation and tutorials on creating own widgets.
```
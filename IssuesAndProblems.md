### Cross platform desktop operations ###
This tasks need cross platform library:
```
- Determine file  MIME, with magic numbers test if possible
```
On Linux/Unix: pyxdg/GIO/gnome-vfs can be used. For other platforms other solution is needed.


---

```
- Get a list of prefered applications for a file
```
On Linux/Unix WM gnome-vfs-python or GIO or pykde4 can be used. Other systems, something more flexible for Linux/Unix?

---

```
- Trashcan/Trash specification
```
Use native OS tras specifications... what are they?


### Terminal access ###
```
1. Use qtermwidget
2. Use solution from Eric IDE
```
qtermwidget is based on Konsole, KDE4 apps run on OS X and Windows. Will Qtermwidget run correctly on Windows?
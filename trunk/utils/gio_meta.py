try:
	import gio
except:
	print '*Optional dependency missing* No GIO python package. Install pygobject if you use GNOME or related WM, for application suggesting and mime detection'

def get_meta_info(filename):
	try:
		filetype = gio.content_type_guess(filename)
		info = gio.app_info_get_all_for_type(filetype)
	except:
		return False
	
	apps = []
	for i in info:
		ret = {}
		ret['name'] = i.get_name()
		ret['description'] = i.get_description()
		ret['exec'] = i.get_executable()
		apps.append(ret)
	
	return apps

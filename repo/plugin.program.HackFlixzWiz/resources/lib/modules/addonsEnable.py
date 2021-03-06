import glob, os, sqlite3
import xbmc, xbmcaddon
from xbmc import log
from addonvar import *
from datetime import datetime
from xml.dom.minidom import parse

addon_xmls = []

def enable_addons():
	for name in glob.glob(os.path.join(addons_path,'*/addon.xml')):
		addon_xmls.append(name)
	addon_xmls.sort()
	addon_ids =[]
	for xml in addon_xmls:
		try:
			root = parse(xml)
			tag = root.documentElement
			_id = tag.getAttribute('id')
			addon_ids.append(_id)
		except:
			pass
	enabled=[]
	disabled=[]
	for x in addon_ids:
		try:
			xbmcaddon.Addon(id = x)
			enabled.append(x)
		except:
			disabled.append(x)
	for y in disabled:
		try:
			enable_db(y)
		except:
			xbmc.executebuiltin(EnableAddon(y))
	addon.setSetting('firstrun', 'false')
	
def enable_db(d_addon):
    """ create a database connection to a SQLite database """
    conn = None
    conn = sqlite3.connect(addons_db)
    c = conn.cursor()
    try:
    	c.execute("SELECT id, addonID, enabled FROM installed WHERE addonID = ?", (d_addon,))
    	found = c.fetchone()
    	if found == None:
    		# Insert a row of data
    		c.execute('INSERT INTO installed (addonID , enabled, installDate) VALUES (?,?,?)', (d_addon, '1', installed_date,))
    	else:
    		c.execute('UPDATE installed SET enabled = ? WHERE addonID = ? ', (1, d_addon,))
    except Exception as e:
    	log('Failed to enable %s. Reason: %s' % (d_addon, e), xbmc.LOGINFO)
    conn.commit()
    conn.close()
import xbmc,xbmcaddon,os
addon_id = 'plugin.video.movie25-mod'
selfAddon = xbmcaddon.Addon(id=addon_id)
# Examples:
#Commands.append(('Add-on settings','XBMC.RunScript('+xbmc.translatePath('special://home/addons/' + addon_id + '/resources/libs/settings.py')+')'))
# or
#Commands.append(('Add-on settings','XBMC.RunScript('+xbmc.translatePath(mashpath + '/resources/libs/settings.py')+')'))
# or
#Commands.append(('[B][COLOR lime]Mash Up[/COLOR] Settings[/B]','XBMC.RunScript('+xbmc.translatePath(mashpath + '/resources/libs/settings.py')+')'))

def getAddOnID():
    d=addon_id
    return d
    
def getHomeItems():
    d=[]
    for x in range(40): 
        d.append(None);
        itemid = str(x + 1)
        if selfAddon.getSetting("homeitems_" +itemid+ "_enabled")== "true":
            d[x]=int(selfAddon.getSetting("homeitems_" + itemid))
    return d

def getRefreshRequiredSettings():
    s=[]
    s.append(selfAddon.getSetting("meta-view"))
    s.append(selfAddon.getSetting("meta-view-tv"))
    s.append(selfAddon.getSetting("groupfavs"))
    s.append(selfAddon.getSetting("skin"))
    s.append(selfAddon.getSetting("stracker"))
    s.append(selfAddon.getSetting("con-view"))
    s.append(selfAddon.getSetting("xpr-view"))
    s.append(selfAddon.getSetting("artwork"))
    s.append(selfAddon.getSetting("ddtv_my"))
    s.append(selfAddon.getSetting("ddtv_hdtv720p"))
    s.append(selfAddon.getSetting("ddtv_webdl720p"))
    s.append(selfAddon.getSetting("ddtv_webdl1080p"))
    s.append(selfAddon.getSetting("ddtv_hdtv480p"))
    s.append(selfAddon.getSetting("ddtv_pdtv"))
    s.append(selfAddon.getSetting("ddtv_dsr"))
    s.append(selfAddon.getSetting("ddtv_dvdrip"))
    return s

def openSettings():
    d = getHomeItems()
    s = getRefreshRequiredSettings()
    selfAddon.openSettings()
    dnew = getHomeItems()
    snew = getRefreshRequiredSettings()
    if d != dnew or s != snew:
        ClearDir(os.path.join(xbmc.translatePath(selfAddon.getAddonInfo('profile')),'Temp'))
        xbmc.executebuiltin("XBMC.Container.Refresh")  

def ClearDir(dir):
    if os.path.exists(dir):
        if os.path.isfile(dir): os.remove(dir)
        else:
            for the_file in os.listdir(dir):
                file_path = os.path.join(dir, the_file)
                try:os.unlink(file_path)
                except Exception, e: print str(e)

if  __name__ == "__main__": openSettings()

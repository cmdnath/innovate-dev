import xbmc,xbmcgui, xbmcaddon, xbmcplugin
import urllib,re,string,os,time,threading
import urllib2

__script__ = 'BW Cinema'
__version__ = '0.1'

print sys.argv[1]
pluginid = int(sys.argv[1])
userName = xbmcplugin.getSetting(pluginid, "username")
userPass = xbmcplugin.getSetting(pluginid, "password")
useRecent = xbmcplugin.getSetting(pluginid, "useRecent")
userRecCnt = int(10)
user_agent = 'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET4.0C; .NET4.0E; InfoPath.3)'
bw_url = 'http://www.bwcinema.com'


def addDir(name, url, mode, iconimage, cookie):
        u = sys.argv[0] + "?url=" + urllib.quote_plus(url) + "&mode=" + str(mode) + "&name=" + urllib.quote_plus(name) + "&cookie=" + urllib.quote_plus(cookie)
        ok = True
        liz = xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
        liz.setInfo(type="Video", infoLabels={ "Title": name })
        ok = xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=u, listitem=liz, isFolder=True)
        return ok
        
addDir('New Releases', 'https://www.bwcinema.com/movies.aspx?reltype=1', 1, '', '') # VG ADD
addDir('Recently Added (' + str(userRecCnt) + ')', 'http://www.bwcinema.com/newmovies.aspx', 1, '', '')
addDir('All Categories', 'http://www.bwcinema.com/Default.aspx', 2, '', '')


addon_id = 'plugin.video.movie25-mod'
selfAddon = xbmcaddon.Addon(id=addon_id)

print selfAddon.getAddonInfo('path')
sys.path.append(os.path.join( xbmc.translatePath( selfAddon.getAddonInfo('path') ), 'resources', 'libs' ) )

try:
    import main,settings    
except Exception, e:
    elogo = xbmc.translatePath('special://home/addons/plugin.video.movie25-mod/resources/art/bigx.png')
    dialog = xbmcgui.Dialog()
    ok=dialog.ok('[B][COLOR=FF67cc33]Movie25-Mod Import Error[/COLOR][/B]','Failed To Import Needed Modules',str(e),'Report missing Module at [COLOR=FF67cc33]https://code.google.com/p/innovate-dev/issues/list[/COLOR] to Fix')
    xbmc.log('Movie25-Mod ERROR - Importing Modules: '+str(e), xbmc.LOGERROR)
              
xbmcplugin.endOfDirectory(int(sys.argv[1]))

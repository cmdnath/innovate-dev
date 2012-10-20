"""
XBMC Addon - Live-Indian-TV
Author : Vineet Gupta
Version : 1.0.0

Change Log : 
1.0.0 : Initial Version
"""

# Step 1 - Load xbmc core support and setup the environment
import urllib
import urllib2
import re
#import xbmcplugin
#import xbmcgui

__script__ = 'Live Indian TV'
__version__ = '0.1'

print(sys.argv[1])
pluginid = int(sys.argv[1])
user_agent = 'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET4.0C; .NET4.0E; InfoPath.3)'
livetv_url = 'http://nowwatchtvlive.com'

def CATEGORIES(url, name):
        req = urllib2.Request(url)
        req.add_header('User-Agent', user_agent)
        response = urllib2.urlopen(req)
        link = response.read()
        response.close()
        
        match = re.compile('class="widget widget_text"><h3>(.+?)</h3>', re.DOTALL).findall(link)

        for name in match:
                addDir(name,livetv_url, 3, '')
        
def INDEX(url, name):
        name=""+name
        req = urllib2.Request(url)
        req.add_header('User-Agent', user_agent)
        response = urllib2.urlopen(req)
        link = response.read()
        response.close()
        match = re.compile('class="widget widget_text"><h3>'+name+'</h3>(.+?)</div></div>', re.DOTALL).findall(link)
        for items in match:
                match1 = re.compile('<li><span style="font-size: small;"><b> <a href="(.+?)">(.+?)</a>(.+?)</b></span></li>', re.DOTALL).findall(items)
                for channelurl, name,spc in match1:
                        addDir(name, channelurl, 4, '')
                        #print channelurl + " " + name
                        #getStreamLink(channelurl, name)
        
def VIDEOLINKS(url, name, thumbnail, cookie):
        req = urllib2.Request(url)
        req.add_header('User-Agent', user_agent)
        req.add_header('Cookie', cookie)
        response = urllib2.urlopen(req)
        link = response.read()
        response.close()

        stream_url = re.compile('<param name="url" value="(.+?)">').findall(link)[0]

        req = urllib2.Request(bw_url + '/' + stream_url)
        req.add_header('User-Agent', 'Mozilla/4.0 (compatible; MSIE 6.0; windows NT 5.1; SV1; .NET CLR 1.1.4322; InfoPath.1; .NET CLR 2.0.50727; windows-media-player/10.00.00.3990)')
        req.add_header('Cookie', cookie)
        response = urllib2.urlopen(req)
        link = response.read()
        response.close()

        addLink(name, link, thumbnail)
                
def get_params():
        param = []
        paramstring = sys.argv[2]
        if len(paramstring) >= 2:
                params = sys.argv[2]
                cleanedparams = params.replace('?', '')
                if (params[len(params) - 1] == '/'):
                        params = params[0:len(params) - 2]
                pairsofparams = cleanedparams.split('&')
                param = {}
                for i in range(len(pairsofparams)):
                        splitparams = {}
                        splitparams = pairsofparams[i].split('=')
                        if (len(splitparams)) == 2:
                                param[splitparams[0]] = splitparams[1]
                                
        return param

def addLink(name, url, iconimage):
        ok = True
        liz = xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
        liz.setInfo(type="Video", infoLabels={ "Title": name })
        ok = xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=url, listitem=liz)
        return ok


def addDir(name, url, mode, iconimage):
        u = sys.argv[0] + "?url=" + urllib.quote_plus(url) + "&mode=" + str(mode) + "&name=" + urllib.quote_plus(name)
        ok = True
        liz = xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
        liz.setInfo(type="Video", infoLabels={ "Title": name })
        ok = xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=u, listitem=liz, isFolder=True)
        return ok
        
              
params = get_params()
url = None
name = None
mode = None

try:
        url = urllib.unquote_plus(params["url"])
except:
        pass
try:
        name = urllib.unquote_plus(params["name"])
except:
        pass
try:
        mode = int(params["mode"])
except:
        pass

print("Mode: " + str(mode))
print("URL: " + str(url))
print("Name: " + str(name))

if mode == None or url == None or len(url) < 1:
        print("")
        CATEGORIES(livetv_url, "")
elif mode == 1:
        RECENTLY_ADDED(url, name)
elif mode == 2:
        CATEGORIES(url, name)
elif mode == 3:
        print("" + url)
        INDEX(url, name)
elif mode == 4:
        print("" + url)
        VIDEOLINKS(url, name, thumbnail)

xbmcplugin.endOfDirectory(int(sys.argv[1]))

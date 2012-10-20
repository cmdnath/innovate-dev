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
import xbmcplugin
import xbmcgui

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
                match1 = re.compile('<span style="font-size: small;">(.+?)<a href="(.+?)">(.+?)</a>(.+?)</span>', re.DOTALL).findall(items)
                for jnk1, channelurl, name,spc in match1:
					try:
							req = urllib2.Request(channelurl)
							response = urllib2.urlopen(req)
							link = response.read()
							response.close()

							match=re.compile('<div class="entry">(.+?)</div></div>', re.DOTALL).findall(link)

							for rawhtml in match:
								playertype=identifyLink(rawhtml, name)
							
							streamLink=getStreamLink(playertype, rawhtml, name)
							addLink(name.title() + "-" + playertype, streamLink, "")
					except:
							pass

def getStreamLink(playertype, rawhtml, name):
        if playertype=="yocast":
                return yocast(rawhtml, name)
		if playertype=="rtmp":
				return rtmp(rawhtml, name)
        else:
                return "None"
        
def identifyLink(rawhtml, name):
        match=re.compile("yocast|cast3d", re.DOTALL).findall(rawhtml)
        if len(match)!=0:
                playertype="yocast"
                return playertype
        match=re.compile("<iframe SRC|<iframe src", re.DOTALL).findall(rawhtml)
        if len(match)!=0:
                playertype="iframe"
                return playertype
        match=re.compile("rtmp",re.DOTALL).findall(rawhtml)
        if len(match)!=0:
                playertype="rtmp"
                return playertype
        match=re.compile("application/x-shockwave-flash",re.DOTALL).findall(rawhtml)
        if len(match)!=0:
                playertype="application/x-shockwave-flash"
                return playertype
        match=re.compile('<iframe name="I5" ', re.DOTALL).findall(rawhtml)
        if len(match)!=0:
                playertype="I5"
                return playertype
        match=re.compile("www.yupptv.com", re.DOTALL).findall(rawhtml)
        if len(match)!=0:
                playertype="yupptv"
                return playertype
        match=re.compile("application/x-mplayer2", re.DOTALL).findall(rawhtml)
        if len(match)!=0:
                playertype="application/x-mplayer2"
                return playertype
        
def yocast(rawhtml, name):
        match = re.compile('<script type=\'text/javascript\'>fid=\'(.+?)\'; (.+?) src=\'(.+?)\'>', re.DOTALL).findall(rawhtml)
        for fid, jnk1, player in match:
                #print fid, player
                streamlink="rtmp://31.204.153.32/app playpath=" + fid + " swfUrl=http://www.yocast.tv/player/player-licensed.swf pageUrl=http://www.yocast.tv/embed.php?live="+fid+"&vw=580&vh=400 live=true swfVfy=true"
        return streamlink

def rtmp(rawhtml, name):
        match = re.compile('<embed src="(.+?)" (.+?)file=(.+?)"(.+?)</embed>', re.DOTALL).findall(rawhtml)
        for player, jnk1, rtmp, jnk2 in match:
                streamlink=rtmp + " swfUrl='"+player+"'"
        return streamlink

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

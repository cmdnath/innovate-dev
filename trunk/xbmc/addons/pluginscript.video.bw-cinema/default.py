"""
XBMC Addon - BW-Cinema
Author : Vineet Gupta
Version : 1.0.0

Change Log : 
1.0.0 : Initial Version
"""

# Step 1 - Load xbmc core support and setup the environment
import urllib,urllib2,re,xbmcplugin,xbmcgui

__script__ = 'BW Cinema'
__version__ = '0.1'

print sys.argv[1]
pluginid = int(sys.argv[1])
userName = xbmcplugin.getSetting(pluginid, "username")
userPass = xbmcplugin.getSetting(pluginid, "password")
useRecent = xbmcplugin.getSetting(pluginid, "useRecent")
userRecCnt = int(xbmcplugin.getSetting(pluginid, "recentCount"))
user_agent = 'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET4.0C; .NET4.0E; InfoPath.3)'
bw_url = 'http://www.bwcinema.com'

'''details={'plot'      : movie.get('summary','') ,
         'title'     : movie.get('title','Unknown').encode('utf-8') ,
         'playcount' : int(movie.get('viewCount',0)) ,
         'rating'    : float(movie.get('rating',0)) ,
         'studio'    : movie.get('studio','') ,
         'mpaa'      : "Rated " + movie.get('contentRating', 'unknown') ,
         'year'      : int(movie.get('year',0)) ,
         'tagline'   : movie.get('tagline','') ,
         'duration'  : str(datetime.timedelta(seconds=duration)) ,
         'overlay'   : _OVERLAY_XBMC_UNWATCHED }
'''

def LOGIN_OVERALL():
        req = urllib2.Request(bw_url + '/login.aspx')
        req.add_header('User-Agent', user_agent)
        response = urllib2.urlopen(req)
        link = response.read()
        info = response.info()
        response.close()

        #Extracting Cookie And Encoding Login
        cookie = info.getheader('Set-Cookie').split(';')[0]
        viewstate = re.compile('<input type="hidden" name="__VIEWSTATE" id="__VIEWSTATE" value="(.+?)" />').findall(link)
        eventvalidation = re.compile('<input type="hidden" name="__EVENTVALIDATION" id="__EVENTVALIDATION" value="(.+?)" />').findall(link)
        logindata = [('__EVENTTARGET', ''), ('__EVENTARGUMENT', ''), ('__VIEWSTATE', viewstate), ('__EVENTVALIDATION', eventvalidation), ('keyword', ''), ('searchIn','movie'), ('txtUserName', userName), ('txtUserPass', userPass), ('btnLogin.x','42'), ('btnLogin.y','15')]
        logindata_enc = urllib.urlencode(logindata,True)

        #Logging In
        req = urllib2.Request(bw_url + '/login.aspx')
        req.add_header('User-Agent', user_agent)
        req.add_header('Cookie', cookie)
        response = urllib2.urlopen(req, logindata_enc)
        print 'Logged in'
        link = response.read()
        response.close()

        if useRecent:
                addDir('New Releases', 'https://www.bwcinema.com/movies.aspx?reltype=1', 1, '', cookie) # VG ADD
                addDir('Recently Added (' + str(userRecCnt) + ')', 'http://www.bwcinema.com/newmovies.aspx', 1, '', cookie)
                addDir('All Categories', 'http://www.bwcinema.com/Default.aspx', 2, '', cookie)
        else:
                CATEGORIES('http://www.bwcinema.com/Default.aspx', cookie)

def RECENTLY_ADDED(url, cookie):
        req = urllib2.Request(url)
        req.add_header('User-Agent', user_agent)
        req.add_header('Cookie', cookie)
        response = urllib2.urlopen(req)
        link = response.read()
        response.close()
        match = re.compile('<span id="MovieList_ct(.+?)_Label1" class="movienamex">(.+?)</span>(.+?)<a href="(.+?)" id=(.+?)class="imgmoviebox" src="(.+?)" align(.+?)<a id="MovieList_ct(.+?)_playLink" href="(.+?)">', re.DOTALL).findall(link)
        if userRecCnt < len(match):
                match = match[0:userRecCnt]
        for cnt1, name, jnk1, moviedetails, jnk2, thumbnail, jnk3, cnt2, url in match:
                #addDir(name, bw_url + '/' + url, 4, bw_url + '/' + thumbnail, cookie)
                VIDEOLINKS(bw_url + '/' + url, name, bw_url + '/' + thumbnail, cookie)


def CATEGORIES(url, cookie):
        req = urllib2.Request(url)
        req.add_header('User-Agent', user_agent)
        req.add_header('Cookie', cookie)
        response = urllib2.urlopen(req)
        link = response.read()
        response.close()
        
        print 'checking categories'
        match = re.compile('<td\s*?class="lmnorm.+?<a.+?href="(.+?)">(.+?)</a>', re.DOTALL).findall(link)
        match = match[0:len(match) - 2]

        for url, name in match:
                fixed_name = re.compile('<font.+?>(.+?)</font>').findall(name)
                if len(fixed_name) < 1:
                    fixed_name = re.sub('\t|\r|\n', '', name)
                else:
                    fixed_name = re.sub('\t|\r|\n', '', fixed_name[0])
                addDir(fixed_name, bw_url + '/' + url, 3, '', cookie)
                       
def INDEX(url, cookie):
        req = urllib2.Request(url)
        req.add_header('User-Agent', user_agent)
        req.add_header('Cookie', cookie)
        response = urllib2.urlopen(req)
        link = response.read()
        response.close()
        match = re.compile('<span id="MovieList__ct.*?_Label1" class="movienamex">(.+?)</span></div>.*?<img id="MovieList__ct.*?_Image1" src="(.+?)".+?<a id="MovieList__ct.*?_playLink" href="(.+?)">', re.DOTALL).findall(link)
        for name, thumbnail, url in match:
                addDir(name, bw_url + '/' + url, 4, bw_url + '/' + thumbnail, cookie)


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


def addDir(name, url, mode, iconimage, cookie):
        u = sys.argv[0] + "?url=" + urllib.quote_plus(url) + "&mode=" + str(mode) + "&name=" + urllib.quote_plus(name) + "&cookie=" + urllib.quote_plus(cookie)
        ok = True
        liz = xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
        liz.setInfo(type="Video", infoLabels={ "Title": name })
        ok = xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=u, listitem=liz, isFolder=True)
        return ok
        
              
params = get_params()
url = None
name = None
mode = None
cookie = None

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
try:
        cookie = urllib.unquote_plus(params["cookie"])
except:
        pass

print "Mode: " + str(mode)
print "URL: " + str(url)
print "Name: " + str(name)

if mode == None or url == None or len(url) < 1:
        print ""
        LOGIN_OVERALL()
elif mode == 1:
        RECENTLY_ADDED(url, cookie)
elif mode == 2:
        CATEGORIES(url, cookie)
elif mode == 3:
        print "" + url
        INDEX(url, name)
elif mode == 4:
        print "" + url
        VIDEOLINKS(url, name, thumbnail, cookie)

xbmcplugin.endOfDirectory(int(sys.argv[1]))

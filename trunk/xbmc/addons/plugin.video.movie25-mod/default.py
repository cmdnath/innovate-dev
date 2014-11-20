import xbmc,xbmcgui, xbmcaddon, xbmcplugin
import urllib,re,string,os,time,threading
import urllib2

addon_id = 'plugin.video.movie25-mod'
selfAddon = xbmcaddon.Addon(id=addon_id)

print selfAddon.getAddonInfo('path')

try:
    from resources.libs import main,settings    
except Exception, e:
    elogo = xbmc.translatePath('special://home/addons/plugin.video.movie25-mod/resources/art/bigx.png')
    dialog = xbmcgui.Dialog()
    ok=dialog.ok('[B][COLOR=FF67cc33]Movie25-Mod Import Error[/COLOR][/B]','Failed To Import Needed Modules',str(e),'Report missing Module at [COLOR=FF67cc33]https://code.google.com/p/innovate-dev/issues/list[/COLOR] to Fix')
    xbmc.log('Movie25-Mod ERROR - Importing Modules: '+str(e), xbmc.LOGERROR)

art = main.art

################################################################################ Directories ##########################################################################################################
CachePath=os.path.join(main.datapath,'Cache')
try: os.makedirs(CachePath)
except: pass
CookiesPath=os.path.join(main.datapath,'Cookies')
try: os.makedirs(CookiesPath)
except: pass
TempPath=os.path.join(main.datapath,'Temp')
try: os.makedirs(TempPath)
except: pass

def AtoZ():
    main.addDir('0-9','http://www.movie25.so/movies/0-9/',1,art+'/09.png')
    for i in string.ascii_uppercase:
            main.addDir(i,'http://www.movie25.so/movies/'+i.lower()+'/',1,art+'/'+i.lower()+'.png')

def MAIN():
    xbmcgui.Window(10000).clearProperty('MASH_SSR_TYPE')
    d = settings.getHomeItems()
    for index, value in sorted(enumerate(d), key=lambda x:x[1]):
        if value==None: continue
        if index==0:
            main.addDirHome('Search','http://www.movie25.so/',420,art+'/search2.png')
        elif index==1:
            main.addDirHome("All Fav's",'http://www.movie25.so/',639,art+'/favsu.png')
        elif index==2:
            main.addDirHome('A-Z','http://www.movie25.so/',6,art+'/az2.png')
        elif index==3:
            main.addDirHome('New Releases','http://www.movie25.so/movies/new-releases/',1,art+'/new2.png')
        elif index==4:
            main.addDirHome('Latest Added','http://www.movie25.so/movies/latest-added/',1,art+'/latest2.png')
        elif index==5:
            main.addDirHome('Featured Movies','http://www.movie25.so/movies/featured-movies/',1,art+'/feat2.png')
        elif index==6:
            main.addDirHome('Most Viewed','http://www.movie25.so/movies/most-viewed/',1,art+'/view2.png')
        elif index==7:
            main.addDirHome('Most Voted','http://www.movie25.so/movies/most-voted/',1,art+'/vote2.png')
        elif index==8:
            main.addDirHome('HD Releases','http://www.movie25.so/movies/latest-hd-movies/',1,art+'/dvd2hd.png')
        elif index==9:
            main.addDirHome('Genre','http://www.movie25.so/',2,art+'/genre2.png')
        elif index==10:
            main.addDirHome('By Year','http://www.movie25.so/',7,art+'/year2.png')
        elif index==11:
            main.addDirHome('Watch History','history',222,art+'/whistory.png')
        elif index==14:
            main.addDirHome('International','http://www.movie25.so/',36,art+'/intl.png')
        elif index==16:
            main.addDirHome('Live Streams','http://www.movie25.so/',115,art+'/live.png')
        elif index==17:
            main.addDirHome('More TV Shows & Movies','http://www.movie25.so/',500,art+'/moretvmovies.png')
        elif index==18:
            main.addDirHome('Anime','http://www.movie25.so/',265,art+'/anime.png')
        elif index==19:
            main.addDirHome('[COLOR=FF67cc33]VIP[/COLOR]laylists','http://www.movie25.so/',234,art+'/vipp.png')
        elif index==20:
            main.addDirHome('Sports','http://www.movie25.so/',43,art+'/sportsec2.png')
        elif index==21:
            main.addDirHome('Adventure','http://www.movie25.so/',63,art+'/adv2.png')
        elif index==22:
            main.addDirHome('Kids Zone','http://www.movie25.so/',76,art+'/kidzone2.png')
        elif index==23:
            main.addDirHome('Documentaries','http://www.movie25.so/',85,art+'/docsec1.png')
    main.addPlayc('MashUp Settings','http://www.movie25.so/',1999,art+'/MashSettings.png','','','','','')

def GENRE(url,index=False):
    main.addDir('Action','http://www.movie25.so/movies/action/',1,art+'/act.png',index=index)
    main.addDir('Adventure','http://www.movie25.so/movies/adventure/',1,art+'/adv.png',index=index)
    main.addDir('Animation','http://www.movie25.so/movies/animation/',1,art+'/ani.png',index=index)
    main.addDir('Biography','http://www.movie25.so/movies/biography/',1,art+'/bio.png',index=index)
    main.addDir('Comedy','http://www.movie25.so/movies/comedy/',1,art+'/com.png',index=index)
    main.addDir('Crime','http://www.movie25.so/movies/crime/',1,art+'/cri.png',index=index)
    main.addDir('Documentary','http://www.movie25.so/movies/documentary/',1,art+'/doc.png',index=index)
    main.addDir('Drama','http://www.movie25.so/movies/drama/',1,art+'/dra.png',index=index)
    main.addDir('Family','http://www.movie25.so/movies/family/',1,art+'/fam.png',index=index)
    main.addDir('Fantasy','http://www.movie25.so/movies/fantasy/',1,art+'/fant.png',index=index)
    main.addDir('History','http://www.movie25.so/movies/history/',1,art+'/his.png',index=index)
    main.addDir('Horror','http://www.movie25.so/movies/horror/',1,art+'/hor.png',index=index)
    main.addDir('Music','http://www.movie25.so/movies/music/',1,art+'/mus.png',index=index)
    main.addDir('Musical','http://www.movie25.so/movies/musical/',1,art+'/mucl.png',index=index)
    main.addDir('Mystery','http://www.movie25.so/movies/mystery/',1,art+'/mys.png',index=index)
    main.addDir('Romance','http://www.movie25.so/movies/romance/',1,art+'/rom.png',index=index)
    main.addDir('Sci-Fi','http://www.movie25.so/movies/sci-fi/',1,art+'/sci.png',index=index)
    main.addDir('Short','http://www.movie25.so/movies/short/',1,art+'/sho.png',index=index)
    main.addDir('Sport','http://www.movie25.so/movies/sport/',1,art+'/sport.png',index=index)
    main.addDir('Thriller','http://www.movie25.so/movies/thriller/',1,art+'/thr.png',index=index)
    main.addDir('War','http://www.movie25.so/movies/war/',1,art+'/war.png',index=index)
    main.addDir('Western','http://www.movie25.so/movies/western/',1,art+'/west.png',index=index)
    main.VIEWSB()
        
def YEAR(index=False):
    main.addDir('2014','http://www.movie25.so/search.php?year=2014/',8,art+'/2014.png',index=index)
    main.addDir('2013','http://www.movie25.so/search.php?year=2013/',8,art+'/2013.png',index=index)
    main.addDir('2012','http://www.movie25.so/search.php?year=2012/',8,art+'/2012.png',index=index)
    main.addDir('2011','http://www.movie25.so/search.php?year=2011/',8,art+'/2011.png',index=index)
    main.addDir('2010','http://www.movie25.so/search.php?year=2010/',8,art+'/2010.png',index=index)
    main.addDir('2009','http://www.movie25.so/search.php?year=2009/',8,art+'/2009.png',index=index)
    main.addDir('2008','http://www.movie25.so/search.php?year=2008/',8,art+'/2008.png',index=index)
    main.addDir('2007','http://www.movie25.so/search.php?year=2007/',8,art+'/2007.png',index=index)
    main.addDir('2006','http://www.movie25.so/search.php?year=2006/',8,art+'/2006.png',index=index)
    main.addDir('2005','http://www.movie25.so/search.php?year=2005/',8,art+'/2005.png',index=index)
    main.addDir('2004','http://www.movie25.so/search.php?year=2004/',8,art+'/2004.png',index=index)
    main.addDir('2003','http://www.movie25.so/search.php?year=2003/',8,art+'/2003.png',index=index)
    main.addDir('Enter Year','http://www.movie25.com',23,art+'/enteryear.png',index=index)
    main.VIEWSB()

def GlobalFav():
    if selfAddon.getSetting("groupfavs") == "true":
        ListglobalFavALL()
    else:
        main.addLink("[COLOR red]Mash Up Fav's can also be favorited under XBMC favorites[/COLOR]",'','')
        main.addDir("Downloaded Content",'Mash Up',241,art+'/downloadlog.png')
        main.addDir("Movie Fav's",'http://www.movie25.so/',641,art+'/fav.png')
        main.addDir("TV Show Fav's",'http://www.movie25.so/',640,art+'/fav.png')
        main.addDir("TV Episode Fav's",'http://www.movie25.so/',651,art+'/fav.png')
        main.addDir("Live Fav's",'http://www.movie25.so/',648,art+'/fav.png')
        main.addDir("Misc. Fav's",'http://www.movie25.so/',650,art+'/fav.png')
    
################################################################################ Modes ##########################################################################################################


def get_params():
    param=[]
    paramstring=sys.argv[2]
    if len(paramstring)>=2:
        params=sys.argv[2]
        cleanedparams=params.replace('?','')
        if (params[len(params)-1]=='/'):
            params=params[0:len(params)-2]
        pairsofparams=cleanedparams.split('&')
        param={}
        for i in range(len(pairsofparams)):
            splitparams={}
            splitparams=pairsofparams[i].split('=')
            if (len(splitparams))==2:
                param[splitparams[0]]=splitparams[1]
    return param
              
params=get_params()

url=None
name=None
mode=None
iconimage=None
fanart=None
plot=None
genre=None
title=None
season=None
episode=None
location=None
path=None
index=None

try: name=urllib.unquote_plus(params["name"])
except: pass
try: url=urllib.unquote_plus(params["url"])
except: pass
try: mode=int(params["mode"])
except: pass
try:
    iconimage=urllib.unquote_plus(params["iconimage"])
    iconimage = iconimage.replace(' ','%20')
except: pass
try: plot=urllib.unquote_plus(params["plot"])
except: pass
try:
    fanart=urllib.unquote_plus(params["fanart"])
    fanart = fanart.replace(' ','%20')
except: pass
try: genre=urllib.unquote_plus(params["genre"])
except: pass
try: title=urllib.unquote_plus(params["title"])
except: pass
try: episode=int(params["episode"])
except: pass
try: season=int(params["season"])
except: pass
try: location=urllib.unquote_plus(params["location"])
except: pass
try: path=urllib.unquote_plus(params["path"])
except: pass
try: index=urllib.unquote_plus(params["index"])
except: pass

print "Mode: "+str(mode)
print "URL: "+str(url)
print "Name: "+str(name)
print "Thumb: "+str(iconimage)

if mode==None or url==None or len(url)<1:
    MAIN()
    main.VIEWSB()        
   
elif mode==1:
    from resources.libs import movie25
    movie25.LISTMOVIES(url,index=index)
    
elif mode==2:
    print ""+url
    GENRE(url,index=index)

elif mode==3:
    from resources.libs import movie25
    print ""+url
    movie25.VIDEOLINKS(name,url)

elif mode==4:
    from resources.libs import movie25
    print ""+url
    movie25.SEARCH(url,index=index)
    

elif mode==5:
    from resources.libs import movie25
    print ""+url
    movie25.PLAY(name,url)

elif mode==6:
    AtoZ(index=index)

elif mode==7:
    YEAR(index=index)

elif mode==8:
    from resources.libs import movie25
    print ""+url
    movie25.YEARB(url,index=index)

elif mode==9:
    from resources.libs import movie25
    print ""+url
    movie25.NEXTPAGE(url,index=index)
    
elif mode==10:
    from resources.libs import movie25
    ListglobalFavM25()

elif mode==11:
    from resources.libs import movie25
    print ""+url
    movie25.GroupedHosts(name,url,iconimage)

elif mode==23:
    from resources.libs import movie25
    movie25.ENTYEAR(index=index)

xbmcplugin.endOfDirectory(int(sys.argv[1]))

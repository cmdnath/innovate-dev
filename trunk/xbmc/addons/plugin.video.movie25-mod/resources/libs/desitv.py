import urllib,re,sys,os
import xbmc, xbmcgui, xbmcaddon, xbmcplugin
import main
import BeautifulSoup

#Mash Up - by Mash2k3 2012.

from resources.libs import settings 
addon_id = settings.getAddOnID()

selfAddon = xbmcaddon.Addon(id=addon_id)
art = main.art
MainUrl='http://www.desirulez.net/'
prettyName='DesiRulez'

def LISTSHOWS(murl,index=False):
    link=main.OPENURL(murl)
    link=link.replace('\r','').replace('\n','').replace('\t','').replace('&nbsp;','')
    match = re.findall('<div class="titleline"><h2 class="forumtitle"><a href="(.+?)">(.+?)</a></h2></div>',link)
    dialogWait = xbmcgui.DialogProgress()
    ret = dialogWait.create('Please wait until TV Show list is cached.')
    totalLinks = len(match)
    loadedLinks = 0
    remaining_display = 'TV Shows loaded :: [B]'+str(loadedLinks)+' / '+str(totalLinks)+'[/B].'
    dialogWait.update(0, '[B]Will load instantly from now on[/B]',remaining_display)
    xbmc.executebuiltin("XBMC.Dialog.Close(busydialog,true)")
    for url,name in match:
        if "color" in name:
            name=name.replace('<b><font color=red>','[COLOR red]').replace('</font></b>','[/COLOR]')
            name=name.replace('<b><font color="red">','[COLOR red]').replace('</font></b>','[/COLOR]')
        main.addTVInfo(name,MainUrl+url,38,'','','')
        loadedLinks = loadedLinks + 1
        percent = (loadedLinks * 100)/totalLinks
        remaining_display = 'TV Shows loaded :: [B]'+str(loadedLinks)+' / '+str(totalLinks)+'[/B].'
        dialogWait.update(percent,'[B]Will load instantly from now on[/B]',remaining_display)
        if dialogWait.iscanceled(): return False   
    dialogWait.close()
    del dialogWait
    xbmcplugin.setContent(int(sys.argv[1]), 'TV Shows')
    main.VIEWS()

def LISTEPISODES(tvshowname,url):
    link=main.OPENURL(url)
    link=link.replace('\r','').replace('\n','').replace('\t','').replace('&nbsp;','')
    match = re.findall('<a class="title threadtitle_unread" href="(.+?)" id=".+?">(.+?)</a>',link)
    if not match:
        match = re.findall('<a class="title" href="(.+?)" id=".+?">(.+?)</a>',link)
    dialogWait = xbmcgui.DialogProgress()
    ret = dialogWait.create('Please wait until ['+tvshowname+'] Episodes are cached.')
    totalLinks = len(match)
    loadedLinks = 0
    remaining_display = 'Episodes loaded :: [B]'+str(loadedLinks)+' / '+str(totalLinks)+'[/B].'
    dialogWait.update(0, '[B]Will load instantly from now on[/B]',remaining_display)
    xbmc.executebuiltin("XBMC.Dialog.Close(busydialog,true)")
    for url,name in match:
        if "Online" not in name: continue
        name=name.replace(tvshowname,'').replace('Watch Online','')
        name=main.removeNonASCII(name)
        main.addTVInfo(name,MainUrl+url,39,'','','') 
        loadedLinks = loadedLinks + 1
        percent = (loadedLinks * 100)/totalLinks
        remaining_display = 'Episodes loaded :: [B]'+str(loadedLinks)+' / '+str(totalLinks)+'[/B].'
        dialogWait.update(percent,'[B]Will load instantly from now on[/B]',remaining_display)
        if dialogWait.iscanceled(): return False   
    match=re.findall('<div id="above_threadlist" class="above_threadlist">(.+?)</div>',link)
    for string in match:
        match1=re.findall('<a href="(.+?)" title="(.+?)">[0-9]+</a>', string)
        for url, page in match1:
            main.addTVInfo(page,MainUrl+url,38,'','','')
    dialogWait.close()
    del dialogWait
    xbmcplugin.setContent(int(sys.argv[1]), 'TV Shows')
    main.VIEWS()

def getVideoSourceIcon(source_name):
    img_url=None
    if re.search('dailymotion',source_name,flags=re.I):
        img_url = 'http://fontslogo.com/wp-content/uploads/2013/02/Dailymotion-LOGO.jpg'
    elif re.search('flash',source_name,flags=re.I):
        img_url = 'http://www.playwire.com/images/logo.png'
    elif re.search('cloud',source_name,flags=re.I):
        img_url = 'http://www.cloudy.ec/img/logo.png'
    return img_url
def VIDEOLINKS(name, url):
    video_source_id = 1
    video_source_name = None
    video_playlist_items = []
    
    link=main.OPENURL(url)
    link=link.replace('\r','').replace('\n','').replace('\t','').replace('&nbsp;','')
    soup = BeautifulSoup.BeautifulSoup(link).findAll('blockquote', {'class':re.compile(r'\bpostcontent\b')})[0]
    for e in soup.findAll('br'):
        e.extract()
        
    if soup.has_key('div'):
        soup = soup.findChild('div', recursive=False)
    for child in soup.findChildren():
        if (child.name == 'font') and re.search('Links',str(child.getText()),re.IGNORECASE):
                if len(video_playlist_items) > 0:
                    main.addPlayList(video_source_name, url,40, video_source_id, video_playlist_items, name, getVideoSourceIcon(video_source_name))
                    video_playlist_items = []
                    video_source_id = video_source_id + 1
                video_source_name = child.getText()
                video_source_name = video_source_name.replace('Online','').replace('Links','').replace('Quality','').replace('  ','')
        elif (child.name =='a') and not child.getText() == 'registration' :
            video_playlist_items.append(str(child['href']))
            
def preparevideolink(video_url, video_source):
    return main.resolve_url(video_url, video_source)
    
def PLAY(name, items, episodeName, video_source):
    video_stream_links = []
    dialog = xbmcgui.DialogProgress()
    dialog.create('Resolving', 'Resolving Aftershock '+video_source+' Link...')       
    dialog.update(0)
    for item in items:
        video_stream_links.append(preparevideolink(item, name))
        dialog.update(100/len(items))
        if dialog.iscanceled(): return None
    if dialog.iscanceled(): return None
    dialog.update(100)
    dialog.close()
    del dialog
    
    from resources.universal import playbackengine
    if len(video_stream_links) > 0:
        playbackengine.PlayAllInPL(episodeName, video_stream_links, img=getVideoSourceIcon(video_source))
        
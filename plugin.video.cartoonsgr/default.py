# -*- coding: utf-8 -*-

import urllib, xbmcgui, xbmcaddon, xbmcplugin, xbmc, re, sys, os
import unshortenit
import resolveurl
from resources.lib.modules import client
from resources.lib.modules import cache
from resources.lib.modules import control
from resources.lib.modules import init
from resources.lib.modules import views

BASEURL = 'https://paidikestainies.online/'
GAMATO = 'https://gamatokids.com/'

ADDON       = xbmcaddon.Addon()
ADDON_DATA  = ADDON.getAddonInfo('profile')
ADDON_PATH  = ADDON.getAddonInfo('path')
DESCRIPTION = ADDON.getAddonInfo('description')
FANART      = ADDON.getAddonInfo('fanart')
ICON        = ADDON.getAddonInfo('icon')
ID          = ADDON.getAddonInfo('id')
NAME        = ADDON.getAddonInfo('name')
VERSION     = ADDON.getAddonInfo('version')
Lang        = ADDON.getLocalizedString
Dialog      = xbmcgui.Dialog()
vers = VERSION
ART = ADDON_PATH + "/resources/icons/"


def Main_addDir():
    addDir('[B][COLOR yellow]' + Lang(32022).encode('utf-8') + '[/COLOR][/B]', BASEURL, 19, ART + 'mas.jpg', FANART, '')
    addDir('[B][COLOR yellow]' + Lang(32005).encode('utf-8') + '[/COLOR][/B]', BASEURL, 8, ART + 'random.jpg', FANART, '')
    addDir('[B][COLOR yellow]' + Lang(32008).encode('utf-8') + '[/COLOR][/B]', BASEURL, 5, ART + 'latest.jpg', FANART, '')
    addDir('[B][COLOR yellow]' + Lang(32004).encode('utf-8') + '[/COLOR][/B]', BASEURL+'quality/metaglotismeno/',
           5, ART + 'dub.jpg', FANART, '')
    addDir('[B][COLOR yellow]' + Lang(32003).encode('utf-8') + '[/COLOR][/B]', BASEURL+'quality/ellinikoi-ypotitloi/',
           5, ART + 'sub.jpg', FANART, '')
    addDir('[B][COLOR yellow]Gamato ' + Lang(32000).encode('utf-8') + '[/COLOR][/B]', '', 20, ART + 'gam.png',
           FANART, '')
    addDir('[B][COLOR yellow]' + Lang(32000).encode('utf-8') + '[/COLOR][/B]', '', 13, ART + 'movies.jpg', FANART, '')
    addDir('[B][COLOR yellow]' + Lang(32001).encode('utf-8') + '[/COLOR][/B]', '', 14, ART + 'tvshows.jpg', FANART, '')
    addDir('[B][COLOR gold]' + Lang(32002).encode('utf-8') + '[/COLOR][/B]', '', 6, ICON, FANART, '')
    addDir('[B][COLOR gold]' + Lang(32020).encode('utf-8') + '[/COLOR][/B]', '', 17, ART + 'set.jpg', FANART, '')
    addDir('[B][COLOR gold]' + Lang(32021).encode('utf-8') + '[/COLOR][/B]', '', 9, ART + 'set.jpg', FANART, '')
    addDir('[B][COLOR gold]' + Lang(32019).encode('utf-8') + ': [COLOR lime]%s[/COLOR][/B]' % vers, '', 'bug',
           ART + 'ver.jpg', FANART, '')
    views.selectView('menu', 'menu-view')


def gamatokids():
    addDir('[B][COLOR yellow]' + Lang(32004).encode('utf-8') + '[/COLOR][/B]', GAMATO + 'genre/μεταγλωτισμένα/',
           4, ART + 'dub.jpg', FANART, '')
    addDir('[B][COLOR yellow]TOP 100[/COLOR][/B]', GAMATO + 'top-imdb', 21, ART + 'top.png', FANART, '')
    addDir('[B][COLOR gold]' + Lang(32002).encode('utf-8') + '[/COLOR][/B]', GAMATO, 18, ICON, FANART, '')
    views.selectView('menu', 'menu-view')


def Peliculas():
    addDir('[B][COLOR orangered]' + Lang(32008).encode('utf-8') + '[/COLOR][/B]',
           BASEURL, 5, ART + 'movies.jpg', FANART, '')
    addDir('[B][COLOR orangered]' + Lang(32006).encode('utf-8') + '[/COLOR][/B]',
           BASEURL, 3, ART + 'genre.jpg', FANART, '')
    addDir('[B][COLOR orangered]' + Lang(32007).encode('utf-8') + '[/COLOR][/B]',
           BASEURL, 15, ART + 'etos.jpg', FANART, '')
    views.selectView('menu', 'menu-view')

def Series():
    addDir('[B][COLOR orangered]' + Lang(32006).encode('utf-8') + '[/COLOR][/B]',
           BASEURL, 7, ART + 'genre.jpg', FANART, '')
    addDir('[B][COLOR orangered]' + Lang(32007).encode('utf-8') + '[/COLOR][/B]',
           BASEURL, 16, ART + 'etos.jpg', FANART, '')
    addDir('[B][COLOR orangered]' + Lang(32010).encode('utf-8') + '[/COLOR][/B]',
           BASEURL + 'tvshows-genre/κινούμενα-σχέδια/', 5, ART + 'tvshows.jpg', FANART, '')
    addDir('[B][COLOR orangered]' + Lang(32009).encode('utf-8') + '[/COLOR][/B]',
           BASEURL + 'tvshows/', 5, ART + 'tvshows.jpg', FANART, '')
    views.selectView('menu', 'menu-view')


def Get_Genres(url): #3
    try:
        r = cache.get(client.request, 120, url)
        r = client.parseDOM(r, 'div', attrs={'id': 'moviehome'})[0]
        r = client.parseDOM(r, 'div', attrs={'class': 'categorias'})[0]
        r = client.parseDOM(r, 'li', attrs={'class': 'cat-item.+?'})
        for post in r:
            try:
                url = client.parseDOM(post, 'a', ret='href')[0]
                name = client.parseDOM(post, 'a')[0]
                name = re.sub('\d{4}', '', name)
                items = client.parseDOM(post, 'span')[0].encode('utf-8')
            except BaseException:
                pass
            name = clear_Title(name).encode('utf-8') + ' ([COLORlime]' + items + '[/COLOR])'
            addDir('[B][COLOR white]%s[/COLOR][/B]' %name,url,5,ART + 'movies.jpg',FANART,'')
    except BaseException:
        pass
    views.selectView('menu', 'menu-view')


def year(url):
    r = cache.get(client.request, 120, url)
    r = client.parseDOM(r, 'div', attrs={'id': 'moviehome'})[0]
    r = client.parseDOM(r, 'div', attrs={'class': 'filtro_y'})[0]
    r = client.parseDOM(r, 'li')
    for post in r:
        try:
            url = client.parseDOM(post, 'a', ret='href')[0]
            year = client.parseDOM(post, 'a')[0].encode('utf-8')
        except BaseException:pass
    
        addDir('[B][COLOR white]%s[/COLOR][/B]' % year,url,5,ART + 'movies.jpg',FANART,'')
    views.selectView('menu', 'menu-view')


def Get_TV_Genres(url): #7
    r = cache.get(client.request, 120, url)
    r = client.parseDOM(r, 'div', attrs={'id': 'serieshome'})[0]
    r = client.parseDOM(r, 'div', attrs={'class': 'categorias'})[0]
    r = client.parseDOM(r, 'li', attrs={'class': 'cat-item.+?'})
    for post in r:
        try:
            url = client.parseDOM(post, 'a', ret='href')[0]
            name = client.parseDOM(post, 'a')[0]
            name = re.sub('\d{4}', '', name)
            items = client.parseDOM(post, 'span')[0].encode('utf-8')
        except BaseException:pass    
        name = clear_Title(name).encode('utf-8') +' ([COLORlime]'+items+'[/COLOR])'
        addDir('[B][COLOR white]%s[/COLOR][/B]' %name,url,5,ART + 'tvshows.jpg',FANART,'')
    views.selectView('menu', 'menu-view')


def year_TV(url):
    r = cache.get(client.request, 120, url)
    r = client.parseDOM(r, 'div', attrs={'id': 'serieshome'})[0]
    r = client.parseDOM(r, 'div', attrs={'class': 'filtro_y'})[0]
    r = client.parseDOM(r, 'li')
    for post in r:
        try:
            url = client.parseDOM(post, 'a', ret='href')[0]
            year = client.parseDOM(post, 'a')[0].encode('utf-8')
        except BaseException:pass
        addDir('[B][COLOR white]%s[/COLOR][/B]' %year,url,5,ART + 'tvshows.jpg',FANART,'')
    views.selectView('menu', 'menu-view')


def Get_random(url):#8
    r = client.request(url)
    r = client.parseDOM(r, 'div', attrs={'id': 'slider1'})[0]
    r = client.parseDOM(r, 'div', attrs={'class': 'item'})
    for post in r:
        try:
            url = client.parseDOM(post, 'a', ret='href')[0]
            icon = client.parseDOM(post, 'img', ret='src')[0]
            name = client.parseDOM(post, 'span', attrs={'class': 'ttps'})[0].encode('utf-8')
            name = re.sub('\d{4}', '', name)
        except BaseException:
            pass
        try:
            year = client.parseDOM(post, 'span', attrs={'class': 'ytps'})[0].encode('utf-8')
        except BaseException:
            year = 'N/A'

        name = clear_Title(name)
        if '/ ' in name:
            name = name.split('/ ')
            name = name[1] + ' ([COLORlime]'+year+'[/COLOR])'
        elif '\ ' in name:
            name = name.split('\ ')
            name = name[1] + ' ([COLORlime]'+year+'[/COLOR])'
        else:
            name = name + ' ([COLORlime]' + year + '[/COLOR])'
        if 'tvshows' in url or 'syllogh' in url:
            addDir('[B][COLOR white]%s[/COLOR][/B]' % name,url,11,icon,FANART,'')
        else:
            addDir('[B][COLOR white]%s[/COLOR][/B]' % name,url,10,icon,FANART,'')
    views.selectView('movies', 'movie-view')


def Get_epoxiakes(url):#19
    try:
        r = client.request(url)
        r = client.parseDOM(r, 'div', attrs={'id': 'slider2'})[0]
        if r is None:
            control.infoDialog('Δεν υπάρχουν διαθέσιμοι τίτλοι αυτήν την περίοδο', NAME, ICON, 7000)
        else:
            r = client.parseDOM(r, 'div', attrs={'class': 'item'})
    except BaseException:
        r = []

    for post in r:
        try:
            url = client.parseDOM(post, 'a', ret='href')[0]
            icon = client.parseDOM(post, 'img', ret='src')[0]
            name = client.parseDOM(post, 'span', attrs={'class': 'ttps'})[0].encode('utf-8')
            name = re.sub('\d{4}', '', name)
        except BaseException:
            pass
        try:
            year = client.parseDOM(post, 'span', attrs={'class': 'ytps'})[0].encode('utf-8')
        except BaseException:
            year = 'N/A'

        name = clear_Title(name)
        if '/ ' in name:
            name = name.split('/ ')
            name = name[1] + ' ([COLORlime]'+year+'[/COLOR])'
        elif '\ ' in name:
            name = name.split('\ ')
            name = name[1] + ' ([COLORlime]'+year+'[/COLOR])'
        else:
            name = name + ' ([COLORlime]' + year + '[/COLOR])'
        if 'tvshows' in url or 'syllogh' in url:
            addDir('[B][COLOR white]%s[/COLOR][/B]' % name,url,11,icon,FANART,'')
        else:
            addDir('[B][COLOR white]%s[/COLOR][/B]' % name,url,10,icon,FANART,'')
    views.selectView('movies', 'movie-view')


def Get_content(url): #5
    r = cache.get(client.request, 4, url)
    data = client.parseDOM(r, 'div', attrs={'id': 'mt-\d+'})
    for post in data:
        try:
            url = client.parseDOM(post, 'a', ret='href')[0]
            icon = client.parseDOM(post, 'img', ret='src')[0]
            name = client.parseDOM(post, 'span', attrs={'class': 'tt'})[0]
            name = re.sub('\d{4}', '', name)
            desc = client.parseDOM(post, 'span', attrs={'class': 'ttx'})[0]
        except BaseException:
            pass
        try:
            year = client.parseDOM(post, 'span', attrs={'class': 'year'})[0].encode('utf-8')
        except BaseException:
            year = 'N/A'
        try:
            calidad = client.parseDOM(post, 'span', attrs={'class': 'calidad2'})[0].encode('utf-8')
            calidad = calidad.replace('Μεταγλωτισμένο', 'Μετ').replace('Ελληνικοί Υπότιτλοι', 'Υποτ')
            if '/' in calidad:
                calidad = Lang(32014).encode('utf-8')
            elif 'Προσ' in calidad:
                calidad = Lang(32017).encode('utf-8')
            elif calidad == 'Μετ':
                calidad = Lang(32015).encode('utf-8')
            else:
                calidad = Lang(32016).encode('utf-8')
        except BaseException:
            calidad = 'N/A'

        desc = clear_Title(desc).encode('utf-8')
        name = clear_Title(name).encode('utf-8')
        if '/ ' in name:
            name = name.split('/ ')
            name = name[1] + ' ([COLORlime]'+year+'[/COLOR])'
        elif '\ ' in name:
            name = name.split('\ ')
            name = name[1] + ' ([COLORlime]'+year+'[/COLOR])'
        else:
            name = name + ' ([COLORlime]' + year + '[/COLOR])'
        if 'tvshows' in url or 'syllogh' in url:
            addDir('[B][COLOR white]{0} [{1}][/COLOR][/B]'.format(name, calidad), url, 11, icon, FANART, desc)
        else:
            addDir('[B][COLOR white]{0} [{1}][/COLOR][/B]'.format(name, calidad), url, 10, icon, FANART, desc)
    try:
        np = re.compile('class="pag_b"><a href="(.+?)"',re.DOTALL).findall(r)
        for url in np:
            page = re.compile('page/(\d+)/',re.DOTALL).findall(url)[0]
            page = '[B][COLORlime]'+page+'[B][COLORwhite])[/B][/COLOR]'
            addDir('[B][COLORgold]>>>' +Lang(32011).encode('utf-8')+ '[/COLOR] [COLORwhite](%s' % page, url, 5, ART + 'next.jpg', FANART,'')
    except BaseException: pass
    views.selectView('movies', 'movie-view')


def Get_links(name, url):#10
    username = control.setting('username')
    password = control.setting('password')
    lcookie = cache.get(_Login, 8, BASEURL, username, password)
    name = re.sub('\)\s*\[.+?]', ')', name)
    r = cache.get(client.request, 2, url, True, True, False, None, None, None, False, None, None, lcookie)
    calidad = client.parseDOM(r, 'span', attrs={'class':'calidad2'})[0]
    calidad = client.replaceHTMLCodes(calidad)
    calidad = calidad.encode('utf-8')
    if 'Προσε' in calidad:
        trailer = Trailer(url)
        addDir('[B][COLOR white]%s | [B][COLOR lime]Trailer[/COLOR][/B]' % name, trailer, 100, iconimage, FANART,'')
    else:
        try:
            back = client.parseDOM(r, 'img', ret='src',attrs={'class': 'cover'})[0]
        except BaseException:
            back = client.parseDOM(r, 'img', ret='src', attrs={'itemprop': 'image'})[0]

        try:
            data = client.parseDOM(r, 'div', attrs={'class': 'tabcontent'})
            links = zip(client.parseDOM(data, 'a', ret='href'),
                        client.parseDOM(data, 'a'))
            description = Sinopsis(url)
            trailer = Trailer(url)
            
            addDir('[B][COLOR white]%s | [B][COLOR lime]Trailer[/COLOR][/B]' % name, trailer, 100, iconimage, back,'')
            for url, host in links:
                host = clear_Title(host).encode('utf-8')
                url = re.sub('http://adf.ly/\d+/', '', url)
                
                if 'buck' in url: continue
                elif 'adf.ly' in url:
                    url = unshortenit.unshorten(str(url))
                    if not url[1] == 200:
                        continue
                    else:
                        url = url[0]
                        
                if 'easybytez' in url: continue
                if 'zippy' in url: continue
                title = '%s [B][COLOR white]| %s[/COLOR][/B]' % (name, host.capitalize())
                addDir(title, url, 100, iconimage, back, str(description))
        except BaseException:
            pass
    views.selectView('movies', 'movie-view')


def _Login(url):
    url += 'wp-content/plugins/theme-my-login/modules/themed-profiles/themed-profiles.js?ver=4.9.5'
    lurl = 'http://paidikestainies.online/login/'
    data = {'log': control.setting('username'),
            'pwd': control.setting('password'),
            'wp-submit': 'Log In',
            'redirect_to': url,
            'instance': '',
            'action': 'login'}
    pdata = urllib.urlencode(data)
    login_cookie = client.request(lurl, post=pdata, referer=url, output='cookie')
    return login_cookie
    

def Get_epis_links(name, url):#11
    lcookie = cache.get(_Login, 4, BASEURL)
    OPEN = cache.get(client.request, 4, url, True, True, False, None, None, None,False,None,None,lcookie)
    #Regex2 = re.compile('<a href="(http[s]?://adf.ly.+?|http[s]?://vidlox.+?|http[s]?://openload.+?|http[s]?://vidto.+?|http[s]?://streamin.+?|http[s]?://flashx.+?)".+?target="_blank".*?>(.*?)</a>', re.DOTALL).findall(OPEN)
    data = client.parseDOM(OPEN, 'td', attrs={'class': 'easySpoilerRow'})
    links = []
    for i in data:
        links += zip(client.parseDOM(i, 'a', ret='href', attrs={'target': '_blank'}),
                    client.parseDOM(i, 'a'))
    description = Sinopsis(url)
    trailer = Trailer(url)
    addDir('[B][COLOR white]%s | [B][COLOR lime]Trailer[/COLOR][/B]' %name,trailer,100,iconimage,FANART,'')
    for url, title in links:
        title = re.sub('\d{4}', '', title)
        title = clear_Title(title)
        title = Lang(32018).encode('utf-8') if title == "" else title.encode('utf-8')
        url = re.sub('http://adf.ly/\d+/', '', url)
        if 'buck' in url: continue
        elif 'adf.ly' in url:
            
            url = unshortenit.unshorten(url)
            
            if not url[1] == 200: continue
            else:
                url = url[0]
                
        if 'easybytez' in url: continue
        if 'zippy' in url: continue

        addDir('[B][COLOR white]%s[/COLOR][/B]' %title, url, 100, iconimage, FANART, str(description))
    views.selectView('movies', 'movie-view')


def Sinopsis(url):
    lcookie = cache.get(_Login, 4, BASEURL)
    OPEN = cache.get(client.request, 4, url, True, True, False, None, None, None,False,None,None,lcookie)
    OPEN = client.parseDOM(OPEN, 'div', attrs={'itemprop':'description'})[0]
    OPEN = OPEN.encode('utf8')
    pattern = ['<div*?>(.+?responsive-tabs">)',
               '<p.*?>(.+?responsive-tabs">)']
    try:
        for pattern in pattern:
            Sinopsis = re.findall(pattern, OPEN, flags=re.DOTALL)
            for part in Sinopsis:
                if 'http' in part:
                    continue
                part = re.sub('<.*?>', '', part)
                part = re.sub('\.\s+', '.', part)
                desc = clear_Title(part)
                return desc
    except BaseException: pass


def Trailer(url):
    lcookie = cache.get(_Login, 4, BASEURL)
    OPEN = cache.get(client.request, 4, url, True, True, False, None, None, None,False,None,None,lcookie)
    patron = 'class="youtube_id.+?src="([^"]+)".+?></iframe>'
    trailer_link = find_single_match(OPEN,patron)
    trailer_link = trailer_link.replace('//www.', 'http://')
    return trailer_link


def search_menu():#6
    addDir(Lang(32024).encode('utf-8'), 'new', 26, ICON, FANART, '')
    try:
        from sqlite3 import dbapi2 as database
    except BaseException:
        from pysqlite2 import dbapi2 as database

    dbcon = database.connect(control.searchFile)
    dbcur = dbcon.cursor()

    try:
        dbcur.execute("""CREATE TABLE IF NOT EXISTS Search (url text, search text)""")
    except BaseException:
        pass

    dbcur.execute("SELECT * FROM Search ORDER BY search")

    lst = []

    delete_option = False
    for (url, search) in dbcur.fetchall():
        domain = 'GAMATOKIDS' if 'gamato' in url else 'PAIDIKESTAINIES'
        title = '[B]%s[/B] - [COLORgold][B]%s[/COLOR][/B]' % (search.encode('utf-8'), domain)
        delete_option = True
        addDir(title, url, 26, ICON, FANART, '')
        lst += [(search)]
    dbcur.close()

    if delete_option:
        addDir(Lang(32039).encode('utf-8'), '', 29, ICON, FANART, '')
    views.selectView('movies', 'movie-view')


def Search(url):
    try:
        from sqlite3 import dbapi2 as database
    except ImportError:
        from pysqlite2 import dbapi2 as database
    if url == 'new':
        keyb = xbmc.Keyboard('', Lang(32002).encode('utf-8'))
        keyb.doModal()
        if keyb.isConfirmed():
            search = urllib.quote_plus(keyb.getText())
            term = urllib.unquote_plus(search).decode('utf-8')

            dbcon = database.connect(control.searchFile)
            dbcur = dbcon.cursor()

            dp = xbmcgui.Dialog()
            select = dp.select('Select Website', ['[COLORgold][B]Paidikestainies[/COLOR][/B]',
                                                  '[COLORgold][B]Gamato-Kids[/COLOR][/B]'])
            if select == 0:
                url = BASEURL + "?s=" + search
                dbcur.execute("DELETE FROM Search WHERE url = ?", (url,))
                dbcur.execute("INSERT INTO Search VALUES (?,?)", (url, term))
                dbcon.commit()
                dbcur.close()
                Get_content(url)

            elif select == 1:
                url = "https://gamatokids.com/?s=%s" % search
                dbcur.execute("DELETE FROM Search WHERE url = ?", (url,))
                dbcur.execute("INSERT INTO Search VALUES (?,?)", (url, term))
                dbcon.commit()
                dbcur.close()
                Search_gamato(url)
            else:
                return
        else:
            return


    else:
        if 'gamato' in url:
            Search_gamato(url)
        else:
            Get_content(url)
    views.selectView('movies', 'movie-view')


def Del_search(url):
    control.busy()
    search = url.split('s=')[1].decode('utf-8')

    try:
        from sqlite3 import dbapi2 as database
    except ImportError:
        from pysqlite2 import dbapi2 as database

    dbcon = database.connect(control.searchFile)
    dbcur = dbcon.cursor()
    dbcur.execute("DELETE FROM Search WHERE search = ?", (search,))
    dbcon.commit()
    dbcur.close()
    xbmc.executebuiltin('Container.Refresh')
    control.idle()



######################
####  GAMATOKIDS  ####
######################

def Search_gamato(url): #18
    control.busy()
    data = cache.get(client.request, 4, url)
    posts = client.parseDOM(data, 'div', attrs={'class': 'result-item'})
    for post in posts:
        link = client.parseDOM(post, 'a', ret='href')[0]
        poster = client.parseDOM(post, 'img', ret='src')[0]
        title = client.parseDOM(post, 'img', ret='alt')[0]
        title = clear_Title(title).encode('utf-8')
        try:
            year = client.parseDOM(data, 'span', attrs={'class': 'year'})[0]
            desc = client.parseDOM(data, 'div', attrs={'class': 'contenido'})[0]
            desc = re.sub('<.+?>', '', desc)
            desc = desc.encode('utf-8', 'ignore')
        except BaseException:
            year = 'N/A'
            desc = 'N/A'

        addDir('[B][COLOR white]{0} [{1}][/COLOR][/B]'.format(title, year), link, 18, poster, FANART, str(desc))

    try:
        np = client.parseDOM(data, 'a', ret='href', attrs={'class': 'arrow_pag'})[-1]
        page = np.split('/')[-1]
        title = '[B][COLORgold]>>>' + Lang(32011).encode('utf-8') + ' [COLORwhite]([COLORlime]%s[/COLOR])[/COLOR][/B]' % page
        addDir(title, np, 4, ART + 'next.jpg', FANART, '')
    except BaseException:
        pass
    control.idle()
    views.selectView('movies', 'movie-view')


def gamato_kids(url): #4
    data = cache.get(client.request, 4, url)
    posts = client.parseDOM(data, 'article', attrs={'class': 'item movies'})
    for post in posts:
        try:
            plot = re.findall('''texto["']>(.+?)</div> <div''', post, re.DOTALL)[0]
        except IndexError:
            plot = 'N/A'
        desc = client.replaceHTMLCodes(plot)
        desc = desc.encode('utf-8', 'ignore')
        try:
            title = client.parseDOM(post, 'h4')[0]
        except BaseException:
            title = client.parseDOM(post, 'img', ret='alt')[0]
        title = clear_Title(title).encode('utf-8')
        link = client.parseDOM(post, 'a', ret='href')[0]
        poster = client.parseDOM(post, 'img', ret='src')[0]

        addDir('[B][COLOR white]{0}[/COLOR][/B]'.format(title), link, 12, poster, FANART, str(desc))
    try:
        np = client.parseDOM(data, 'a', ret='href', attrs={'class': 'arrow_pag'})[-1]
        page = np[-2] if np.endswith('/') else re.findall('page/(\d+)/', np)[0]
        title = '[B][COLORgold]>>>' + Lang(32011).encode('utf-8') + ' [COLORwhite]([COLORlime]%s[/COLOR])[/COLOR][/B]' % page
        addDir(title, np.encode('utf-8'), 4, ART + 'next.jpg', FANART, '')
    except BaseException:
        pass
    views.selectView('movies', 'movie-view')


def gamatokids_top(url):
    data = cache.get(client.request, 4, url)
    posts = client.parseDOM(data, 'div', attrs={'class': 'top-imdb-item'})
    for post in posts:
        try:
            title = client.parseDOM(post, 'a')[-1]

            title = clear_Title(title).encode('utf-8')
            link = client.parseDOM(post, 'a', ret='href')[0]
            poster = client.parseDOM(post, 'img', ret='src')[0]

            addDir('[B][COLOR white]{0}[/COLOR][/B]'.format(title), link, 12, poster, FANART, 'Top 100 IMDB')
        except BaseException:
            pass
    views.selectView('movies', 'movie-view')


def gamato_links(url, name, poster): #12
    try:
        data = cache.get(client.request, 4, url)
        desc = client.parseDOM(data, 'div', attrs={'itemprop': 'description'})[0]
        desc = re.sub('<.+?>', '', desc)
        desc = desc.encode('utf-8', 'ignore')
        try:
            match = re.findall('''file\s*:\s*['"](.+?)['"],poster\s*:\s*['"](.+?)['"]\}''', data, re.DOTALL)[0]
            link, _poster = match[0], match[1]
        except BaseException:
            match = re.findall('''file\s*:\s*['"](.+?)['"]\}''', data, re.DOTALL)[0]
            link, _poster = match, poster

        try:
            fanart = client.parseDOM(data, 'div', attrs={'class': 'g-item'})[0]
            fanart = client.parseDOM(fanart, 'a', ret='href')[0]
        except BaseException:
            fanart = FANART
        try:
            trailer = client.parseDOM(data, 'div', attrs={'id': 'trailer'})[0]
            trailer = client.parseDOM(trailer, 'iframe', ret='src')[0]
            addDir('[B][COLOR lime]Trailer[/COLOR][/B]', trailer, 100, iconimage, fanart, str(desc))
        except BaseException:
            pass

        addDir(name, link, 100, poster, fanart, str(desc))
    except BaseException:
        return
    views.selectView('movies', 'movie-view')


########################################

def find_single_match(data, patron, index=0):
    try:
        matches = re.findall(patron, data, flags=re.DOTALL)
        return matches[index]
    except BaseException:
        return ""


def clear_Title(txt):
    txt = re.sub('<.+?>', '', txt)
    txt = txt.replace("&quot;", "\"").replace('()','').replace("&#038;", "&").replace('&#8211;',':').replace('\n',' ')
    txt = txt.replace("&amp;", "&").replace('&#8217;',"'").replace('&#039;',':').replace('&#;','\'')
    txt = txt.replace("&#38;", "&").replace('&#8221;','"').replace('&#8216;','"').replace('&#160;','')
    txt = txt.replace("&nbsp;", "").replace('&#8220;','"').replace('&#8216;','"').replace('\t',' ')
    return txt


def Open_settings():
    control.openSettings()


def cache_clear():
    cache.clear(withyes=False)


def search_clear():
    cache.delete(control.searchFile, withyes=False)
    control.refresh()
    control.idle()


def addDir(name, url, mode, iconimage, fanart, description):
    if mode == 6:
        u = '%s?url=%s&mode=%s&name=%s&iconimage=%s&description=%s' % \
            (sys.argv[0], urllib.quote_plus(url), str(mode), urllib.unquote(name),
             urllib.quote_plus(iconimage), urllib.quote_plus(description))

    else:
        u = sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&iconimage="+urllib.quote_plus(iconimage)+"&description="+urllib.quote_plus(description)
    ok = True
    liz = xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
    liz.setInfo(type="Video", infoLabels={"Title": name, "Plot": description})
    liz.setProperty('fanart_image', fanart)
    cm = []
    cm.append((Lang(32020).encode('utf-8'), "RunPlugin(%s?mode=17)" % init.sysaddon))
    cm.append((Lang(32021).encode('utf-8'), "RunPlugin(%s?mode=9)" % init.sysaddon))

    if mode == 100:
        liz.setProperty("IsPlayable", "true")
        cm.append(('GRecoTM Pair Tool', 'RunAddon(script.grecotm.pair)'))
        liz.addContextMenuItems(cm)
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=u, listitem=liz, isFolder=False)
    elif mode == 9 or mode == 17 or mode == 'bug' or mode == 29:
        ok = xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=u, listitem=liz, isFolder=False)

    elif mode == 26:
        cm.append((Lang(32039).encode('utf-8'), "RunPlugin(%s?mode=%s&url=%s)" % (init.sysaddon, 28, url)))
        liz.addContextMenuItems(cm)
        ok = xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=u, listitem=liz, isFolder=True)

    else:
        liz.addContextMenuItems(cm)
        ok = xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=u, listitem=liz, isFolder=True)
    return ok


def resolve(name, url, iconimage, description):
    host = url
    if host.endswith('mp4') and 'tainies' in host:
        stream_url = host + '|User-Agent=%s&Referer=%s' % (urllib.quote_plus(client.agent(), ':/'), GAMATO)
        name = name
    else:
        stream_url = evaluate(host)
        name = name.split(' [B]|')[0]
    try:
        liz = xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
        liz.setInfo(type="Video", infoLabels={"Title": name, "Plot": description})
        liz.setProperty("IsPlayable","true")
        liz.setPath(str(stream_url))
        xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, liz)
    except BaseException:
        control.infoDialog(Lang(32012), NAME)


def evaluate(host):
    try:
        if 'openload' in host:
            try:
                from resources.lib.resolvers import openload
                host = openload.get_video_openload(host)
                return host
            except BaseException:
                host = resolveurl.resolve(host)

        elif resolveurl.HostedMediaFile(host):
            host = resolveurl.resolve(host)

        return host
    except BaseException:
        pass


params = init.params
url = None
name = None
iconimage = ICON
mode = None
fanart = FANART
description = DESCRIPTION
query = None

try:
        url = urllib.unquote_plus(params["url"])
except BaseException:
        pass
try:
        name = urllib.unquote_plus(params["name"])
except BaseException:
        pass
try:
        iconimage = urllib.unquote_plus(params["iconimage"])
except BaseException:
        pass
try:        
        mode = int(params["mode"])
except BaseException:
        pass
try:        
        fanart = urllib.unquote_plus(params["fanart"])
except BaseException:
        pass
try:        
        description = urllib.unquote_plus(params["description"])
except BaseException:
        pass


print str(ADDON_PATH)+': '+str(VERSION)
print "Mode: "+str(mode)
print "URL: "+str(url)
print "Name: "+str(name)
print "IconImage: "+str(iconimage)
#########################################################

if mode is None:
    Main_addDir()

###############GAMATOKIDS#################
elif mode == 4:
    gamato_kids(url)
elif mode == 12:
    gamato_links(url, name, iconimage)
elif mode == 18:
    Search_gamato(url)
elif mode == 20:
    gamatokids()
elif mode == 21:
    gamatokids_top(url)
##########################################

elif mode == 3:
    Get_Genres(url)
elif mode == 5:
    Get_content(url)
elif mode == 6:
    search_menu()
elif mode == 26:
    Search(url)
elif mode == 29:
    search_clear()
elif mode == 28:
    Del_search(url)
elif mode == 7:
    Get_TV_Genres(url)
elif mode == 8:
    Get_random(url)
elif mode == 9:
    cache_clear()
elif mode == 10:
    Get_links(name, url)
elif mode == 11:
    Get_epis_links(name, url)
elif mode == 13:
    Peliculas()
elif mode == 14:
    Series()
elif mode == 15:
    year(url)
elif mode == 16:
    year_TV(url)
elif mode == 17:
    Open_settings()
elif mode == 19:
    Get_epoxiakes(url)
elif mode == 100:
    resolve(name, url, iconimage, description)

xbmcplugin.endOfDirectory(int(sys.argv[1]))

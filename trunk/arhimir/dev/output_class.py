#coding: UTF-8
from google.appengine.ext import webapp
from google.appengine.ext import db
from google.appengine.api import memcache
from google.appengine.ext.webapp import template
from session_handler import SessionHandler
from tools.scroll import AjaxScroll
from comments.comments import Comments
from db_entities.custom_field import DBCustomField
from db_entities.stat_daily_users import DBDailyUsers
from random import choice as rndchoice
from time import clock, time
from message.handler import Handler as message_handler
import pickle
import re

class OutputClass(webapp.RequestHandler):
    
    version = 14
    request_time = ""
    response_html = False
    is_mainpage = False
    def __init__(self, *args, **kwargs):
        self._child_get = self.get
        self.get = self._get_request_time
        self._child_post = self.post
        self.post = self._post
        try:
            tpls = DBCustomField.gql("where type=4")
            self.__TemplatePath = tpls[0].value.encode("utf8")
        except: self.__TemplatePath = 'templates/'
#        webapp.RequestHandler.__init__(self, *args, **kwargs)
    
    def _post(self, *args, **kwargs):
        self._child_post(*args, **kwargs)
        if self.response_html: self._drawPage(self.title)
    
    def _get_request_time(self, *args, **kwargs):
        time_start = time()
        clock_start = clock()
        self._child_get(*args, **kwargs)
        time_elapsed = (time() - time_start) * 1000
        clock_elapsed = (clock() - clock_start) * 1000
        self.request_time = "Запрос занял %5.0fмс (потрачено процессорного времени: %.0fмс)" % (time_elapsed, clock_elapsed)
        if self.response_html: self._drawPage(self.title)
        if self.is_mainpage: self._drawMainPage()
        
    __pageaccessRights = { 'admin'       : 5, }
    
    __accessRights = { 'eventadd'        : 5,
                       'eventedit'       : 8, }
    
    accessNames = [ { 'access' : -1, 
                      'name' : 'Все' },
                    { 'access' : 5,
                      'name' : 'Менеджеры событий и администраторы' }, 
                    { 'access' : 8,
                      'name' : 'Администраторы и модераторы' },
                    { 'access' : 10,
                      'name' : 'Только администраторы' }, ]
    
    Session = { 'authorized'    : False,
                'name'          : False,
                'surname'       : False,
                'email'         : False,
                'userid'        : 0,
                'access'        : -1,
                'user_key'      : False, }
    
    __ContentOfMainTemplate = ''
    
    def get(self, id=0, redirect=True):
        self.checkSession(self.request.headers.get('Cookie'), redirect)
        if (not self.Session['access'] >= self.access) and (not int(id) == self.Session['userid']) :
            self.showMessage("У вас нет прав на выполнение этого действия")
            return False
        else:
            return True
    
    def checkAccess(self, type):
        return True if self.Session['access'] >= self.__accessRights[type] else False
        
    def __userAccess(self):
        temp_uri = self.request.uri
        url_list = temp_uri.split('/')
        access = True
        for url in url_list:
            if self.__pageaccessRights.has_key(url):
                if self.Session['access'] >= self.__pageaccessRights[url]:
                    access = True
                else:
                    access = False
        return access
    
    def insertScroll(self):
        try:
            s = AjaxScroll()
            return s.render()
        except: return "Техработы на сайте. Скоро мы по...заработаем"
    
    def insertFckEdit(self, Name, Value = "", ToolbarSet = "Basic"):
#        oFCKeditor = fckeditor.FCKeditor(Name, Value, ToolbarSet)
#        editor = oFCKeditor.Create()
        return """
<textarea name=\"""" + Name + """\">""" + Value + """</textarea>
<script type="text/javascript">
    $(document).ready(function() {
        CKEDITOR.replace( '""" + Name + """', { toolbar : '""" + ToolbarSet + """'} );
    });
</script>"""
    
    def insertMenu(self, page = ""):
        if self.Session['authorized'] == True:
            access = {
                        'show_menu_customizing_elements'    :   False,
                        'event'                             :   False,
                        'users'                             :   False,
                        'pages'                             :   False,
                        'news'                              :   False,
                        'customize'                         :   False,
                        'objects'                           :   False,
                        'album'                             :   False,
                        'statistics'                        :   False,
                     }
            if self.Session['access']>=5:
                access['show_menu_customizing_elements'] = True
                access['objects'] = True
                access['album'] = True
            if self.Session['access']>=8:
                access['event'] = True
                access['news'] = True
                access['statistics'] = True
            if self.Session['access']>=10:
                access['users'] = True
                access['pages'] = True
                access['customize'] = True
                
            self.insertTemplate('tpl_menu.html', {
                                                    'name'      :   self.Session['name'],
                                                    'surname'   :   self.Session['surname'],
                                                    'access'    :   access,
                                                    'userid'    :   self.Session['userid'],
                                                    'page'      :   page,
                                                 })
        else:
            self.insertContent("""<form method="post" action="/login/">
            <table>
            <tr>
                <td><font size=1>Логин</font></td><td><font size=1>Пароль</font></td><td>&nbsp;</td>
            </tr>
            <tr>
                <td><input type=text name="login" style="width: 100px; height: 25px;"></td>
                <td><input type=password name="password" style="width: 100px; height: 25px;"</td>
                <td><input value="Войти в систему" type="submit"></td>
            </tr>
            </table>
            </form>""")
        
    def checkSession(self, Cookie, redirect=True):
        self.Session['authorized'] = False
        sh = SessionHandler()
        self.Session = sh.getSessionInfo(Cookie)
        if not (self.Session['authorized'] and self.__userAccess()) and redirect:
            self.redirect("/login/?return="+self.request.uri)
        else:
            data = memcache.get("user_activity_" + str(self.Session['userid']))
            if data is not None:
                memcache.delete("user_activity_" + str(self.Session['userid']))
            else:
                if self.Session['userid']>0:
                    query = db.GqlQuery("SELECT __key__ FROM DBDailyUsers WHERE userid = :userid AND date = :date",
                                          userid = self.Session['userid'],
                                          date = db.datetime.date.today())
                    if query.count() == 0:
                        daily_users = DBDailyUsers()
                        daily_users.login = self.Session['login']
                        daily_users.userid = self.Session['userid']
                        daily_users.put()
            memcache.add("user_activity_" + str(self.Session['userid']), str(self.Session['login']), 300)
            
        return self.Session['authorized']
    
    def destroySession(self):
        self.checkSession(self.request.headers.get('Cookie'), False)
        sh = SessionHandler()
        try: 
            memcache.delete("user_activity_" + self.Session['login']) 
        except: 
            pass
        sh.destroySession(self.Session['sid'])
        self.response.headers.add_header("Set-Cookie", "sid=sessiondestroyed; path=/")
   
    
    def insertContent(self, Template):
        self.__ContentOfMainTemplate += Template
    
    def _drawMainPage(self):
        data = memcache.get("main_page")
        if data:
            self.response.out.write(pickle.loads(data))
        else:
            self.insertTemplate('tpl_new_main.html', { 'scroll' : self._scroll,
                                                       'news' : self._news,
                                                       'tags' : self._tags,
                                                       'events' : self._events,
                                                       'confs' : self._confs,
                                                       'arhs' : self._arhs, 
                                                       'request_time' : self.request_time if self.Session['access'] == 10 else ""
                                                     })
            minified_html = self.minified(self.__ContentOfMainTemplate)
            self.response.out.write(minified_html)
            memcache.add("main_page", pickle.dumps(minified_html), 300)

    def drawMainPage(self, scroll, news, tags, events, confs, arhs):
        self.is_mainpage = True
        self._scroll = scroll
        self._news = news
        self._tags = tags
        self._events = events
        self._confs = confs
        self._arhs = arhs
    
    def drawContent(self):
        self.response.out.write(self.minified(self.__ContentOfMainTemplate))
    
    def drawPage(self, title = ""):
        self.response_html = True
        self.title = title
    
    def _drawPage(self, title = ""):
        #m_class = DBMSG()
        messageinfo = '<div style="margin-top: 2px;"><a href=/message/><b>Новое сообщение!</b></a></div>' if message_handler().has_unread_msg(self.Session['user_key']) else ""
        loginfo = """<div style="float: left; margin-right: 10px; width: 50px; height: 50px; padding: 2px; border-style: solid; border-width: 1px;"><img width="50" height="50" src="/show_avatara/""" + str(self.Session['userid']) +"""" /></div>        
            <div>Добро пожаловать, <b><a class="loginfo" href="/users/""" + self.Session['login'].encode("utf8") + """">""" + self.Session['login'].encode("utf8") + """</a></b></div> """ + messageinfo + """ 
            <div style="margin-top: 2px;"><a class="loginfo" href="/news/">Ваш личный кабинет</a></div>
            <div style="margin-top: 2px;"><a class="loginfo" href="/logout/">Выйти</a></div>
        
        """ if self.Session['authorized'] == True else """ssd"""
        html = template.render(self.__TemplatePath + 'tpl_html.html',
                               { 
                                   'content' : self.__ContentOfMainTemplate,
                                   'version' : 'Engine version: ' + str(self.version),
                                   'loginfo' : loginfo,
                                   #'news': DBNews ().getItems(5),
                                   'authorized' : self.Session['authorized'],
                                   'title' : title,
                                   'request_time' : self.request_time if self.Session['access'] == 10 else ""
                                })
        #cache_name = hashlib.md5(html).hexdigest()
        #data = memcache.get(cache_name)
        #if data:
            #self.response.out.write(pickle.loads(data))
        #else:
        self.response.out.write(self.minified(html))
        #   memcache.add(cache_name, pickle.dumps(minified_html), 300)
    
    def minified(self, html):
        # Вырезаем спецсимволы
        minified_html = re.sub(r'\t|\n|\r', '', html)
        # Правильно вырезаем лишние пробелы
        minified_html = re.sub(r' +', ' ', minified_html)
        # Вырезаем комментарии
        minified_html = re.sub(r'<!--[\s\S]*?-->', '', minified_html)
        return minified_html

    def insertComments(self, entity):
        ch = Comments()
        comments = ch.getComments(entity)
        self.insertTemplate('tpl_comments.html', { 
                                                    'entity' : entity,
                                                    'comments' : comments,
                                                    'admin' : True if self.Session['access'] > 9 else False,
                                                    'logged' : True if self.Session['access'] > -1 else False,
                                                    'login' : self.Session['login'],
                                                    'url' : self.request.uri
                                                 })
        
    def insertTemplate(self, tpl_filename, val = {}):
        self.__ContentOfMainTemplate += template.render(self.__TemplatePath + tpl_filename, val)

    def showMessage(self, message_text):
        self.insertContent("""
        <form id="show_message" action="/msgbox/" method="POST"><input name="message_text" type="hidden" value=\"""" + message_text + """\" /></form>
        <script>
            $(document).ready(function() {
                $("#show_message").submit();
            });
        </script>
        """)
        self.drawPage()
#    def paramByType (self, type):
#        return DBCustomField().getByType(type)
    
    def paramByName (self, name):
        return DBCustomField().getByName(name)
    
    def get_url_part(self, num):
        return self.request.uri.split('/')[num*(-1)]
    
    def random_from_entity(self, entity, count):
        rnd_records = []
        entity_count = entity.all().count()
        if entity_count < count: count = entity_count
        rnd_numbers = [i for i in range(entity_count)]
        while(len(rnd_records)<count):
            rnd_number = rndchoice(rnd_numbers)
            del rnd_numbers[rnd_numbers.index(rnd_number)]
            rnd_records.append(entity.all().fetch(1,rnd_number)[0])
        return rnd_records
    
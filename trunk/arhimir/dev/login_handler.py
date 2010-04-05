#coding: UTF-8
from google.appengine.ext import db
import hashlib
import cgi
from session_handler import SessionHandler
from output_class import OutputClass
from datetime import date, timedelta

class LoginHandler(OutputClass):
    """ User auth """
    
    url_handler = '/login/?|/logout/?'
    
    def get(self):
        self.insertTemplate('tpl_login.html', {'openlogin' : True})
        self.drawPage()
        if self.request.uri.endswith('/logout/'):
            try:
                self.destroySession()
            except:
                pass
            self.redirect('/')
        
    def post(self):
        try:
            self.dbusers = db.GqlQuery("SELECT * FROM DBUser WHERE login = :login AND password = :password",
                                       login = cgi.escape(self.request.get('login')).lower(),
                                       password = hashlib.md5(self.request.get('password')).hexdigest())
        except:
            self.response.out.write("Database error")
            return
        sh = SessionHandler()
        Session = { 'authorized'     : False }
        for dbuser in self.dbusers:
            Session = sh.createSession(int(dbuser.key().id()), self.request.headers.get('Cookie'), str(dbuser.login).lower())
            if dbuser.confirmation:
                if not str(dbuser.confirmation) == '':
                    self.insertContent('Пожалуйста, активируйте свою учетную запись.<br>Для активации учетной записи вам было выслано письмо на указанный при регистрации e-mail.')
                    self.drawPage()
                    return
        if Session['authorized']:
            cookie_expire_date = date.today() + timedelta(days=+7)
            self.response.headers.add_header("Set-Cookie", "sid=" + str(Session['sid']) + "; expires=" + cookie_expire_date.strftime("%a, %d-%b-%Y %H:%M:%S GMT") + "; path=/; HttpOnly")
            temp_uri = self.request.uri
            uri = temp_uri.split('=')
            
            try:
                return_path = str(cgi.escape(uri[-1])) if str(cgi.escape(uri[-2])).find("?return")>0 else '/'
            except:
                return_path = '/' 
            self.redirect(return_path)
        else:
            self.insertContent("""Логин или пароль введены неверно.<br>
            <a href=/>Вернуться на главную</a>
            """)
            self.drawPage("Вход в систему")
            
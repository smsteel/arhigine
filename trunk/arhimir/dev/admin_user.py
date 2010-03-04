# -*- coding: UTF-8 -*-﻿﻿
from google.appengine.ext import db
from output_class import OutputClass
import cgi
from db_entities.user import DBUser
from db_entities.user_picture import DBAvatara
import hashlib, random
from google.appengine.api import images
from register_confirm import RegisterConfirm

class AdminUser(OutputClass):
    
    url_handler = '/user/.*|/changeinfo/.*|/admin/users/?|/admin/objects/add/user/?'
    
    def get(self):
        self.checkSession(self.request.headers.get('Cookie'))
        self.insertMenu()
        temp_uri = self.request.uri
        uri = temp_uri.split('/')
        userid = ""
        try:
            userid = int(cgi.escape(uri[-1]))
        except: pass
        if not (userid == self.Session['userid'] or self.Session['access'] >= 8):
            self.insertContent("""У вас нет прав на выполнение этого действия.""")
            self.drawPage()
            return
            
        if userid != "":
            user = DBUser.get_by_id(int(userid))
            self.insertTemplate('tpl_register.html', { 'title'      : 'Изменение данных пользователя', 
                                                                       'button'     : 'Изменить',
                                                                       'action'     : 'changeinfo',
                                                                       'login'      : str(user.login),
                                                                       'name'       : user.name,
                                                                       'surname'    : user.surname,
                                                                       'email'      : str(user.email),
                                                                       'twitter'    : str(user.twitter) if user.twitter else "",
                                                                       'livejournal': str(user.livejournal) if user.livejournal else "",
                                                                       'userid'     : str(userid),
                                                                       'user_about' : user.about.encode("utf8") if user.about else "",
                                                                       'check'      : True,
                                                                       'checkpwd'   : True,
                                                                       'approve'    : True if userid == self.Session['userid'] and self.Session['access'] < 5 else False, })
        else:
            self.insertTemplate('tpl_admin_user.html', { })
        self.drawPage()
        
    def post(self):
        self.checkSession(self.request.headers.get('Cookie'))
        login = str(self.request.get('logins'))
        if login != "":
            responsehtml = ''
            dbusers = db.GqlQuery("SELECT * FROM DBUser")
            max_users_in_list = 4
            for dbuser in dbusers:
                if str(dbuser.login).find(login) >= 0 and max_users_in_list:
                    max_users_in_list -= 1
                    if str(self.request.get("objectadd")) == "true":
                        responsehtml += "<a style='cursor: pointer;' id='user" + str(max_users_in_list) + "' onclick='$(\"#login\").attr(\"value\", $(\"#user" + str(max_users_in_list) + "\").text()); $(\"#showlogins\").hide();'>" + str(dbuser.login) + "</a><br>"
                    else:
                        responsehtml += "<a href=/changeinfo/" + str(dbuser.key().id()) + ">" + str(dbuser.login) + "</a><br>"
            if login != "": self.response.out.write(responsehtml)
        else:
            
            need_delete = bool(self.request.get('delete'))
            if not need_delete:
                avatara = DBAvatara()
                data = self.request.get("img")
                if data:
                    try:
                        dbQuery = DBAvatara.gql("WHERE userid = :dbuserid", 
                                                dbuserid = int(self.request.get('userid')))
                        avataras = dbQuery.fetch(1)
                        avatara = avataras[0]
                        avatar = images.resize(data, 128, 128)
                        avatara.image = db.Blob(avatar)
                        avatara.put()
                    except:
                        avatar = images.resize(data, 128, 128)
                        avatara.image = db.Blob(avatar)
                        avatara.userid = int(self.request.get('userid'))
                        avatara.put()
            else:
                dbQuery = db.GqlQuery("SELECT __key__ FROM DBAvatara WHERE userid = :dbuserid", 
                                      dbuserid = int(self.request.get('userid')))
                db.delete(dbQuery)
                
            user = DBUser.get_by_id(int(self.request.get('userid')))
            #editeduser = DBUser()
            user.name = cgi.escape(self.request.get('name'))
            user.surname = cgi.escape(self.request.get('surname'))
            user.about = cgi.escape(self.request.get('user_about'))
            user.twitter = cgi.escape(self.request.get('twitter'))
            user.livejournal = cgi.escape(self.request.get('livejournal'))
            answer = '<h1>Данные изменены</h1><br>'
            self.insertMenu()
            if user.email != self.request.get('email'):
                user.email = self.request.get('email')
                confirmation = hashlib.md5(str(random.random())).hexdigest()
                dbuser.confirmation = confirmation
                rc = RegisterConfirm()
                rc.sendEmailCheck(self.request.get('email'), confirmation)
                answer += '<h1>Почта была изменена и на новый адрес было выслано письмо для подтверждения регистрации</h1>'
            if self.request.get('password') != '':
                if(user.password == self.request.get('oldpassword')):
                    user.password = hashlib.md5(self.request.get('password')).hexdigest()
                else:
                    self.insertContent('<h1>Пароль не был изменен</h1><br>')
            user.put()
            
            self.insertContent('<h1>Данные изменены</h1>')
            self.drawPage()
            #db.delete(dbQuery)
            

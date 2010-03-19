# -*- coding: UTF-8 -*-﻿﻿
from google.appengine.ext import db
import cgi
from db_entities.gallery_object import DBGalleryObject
from output_class import OutputClass
from login_handler import LoginHandler
from twitter.twitt_get import TwittGet
from db_entities.user import DBUser

class UserInfo(OutputClass):
    """ guess who """
    
    url_handler = '/users/.*'
    
    def get(self):
        user = str(cgi.escape(self.request.uri.split('/')[-1])).replace("%40", "@")
        if self.checkSession(self.request.headers.get('Cookie'), False):
            self.insertMenu()
        dbuser = db.GqlQuery("SELECT * FROM DBUser where login = :login",
                             login = user)
        for user in dbuser:
            objects_count = 0
            objects_list = ""
            if user.access == 5 or user.access == 6:
                objects = db.Query(DBGalleryObject)
                objects.filter("userid =", int(user.key().id()))
#                objects.order("date")
                objects_count = objects.count()
                for object in objects:
                    objects_list += """<div style="padding: 20px 0px 0px 20px; float: left;"><a href="/objects/""" + str(object.key().id()) + """"><div style="border-width: 1px; border-color: #555555; border-style: solid; padding: 2px;"><img style="border: 0;" src="/picture/130/crop/0/""" + str(object.key().id()) + """" /></div></a></div>"""
                
            twitt = False    
            try:
                t = TwittGet(user.twitter.encode("utf8"))
                twitt = t.get_last_twitt()
            except: pass

            self.insertTemplate('tpl_user_info.html', { 
                                                                   'id' :  str(user.key().id()),
                                                                   'name' : user.name.encode("utf8"),
                                                                   'surname' : user.surname.encode("utf8"),
                                                                   'login' : user.login.encode("utf8"),
                                                                   'comments' : DBUser().count_comments(user.key()),
                                                                   'architect' : True if user.access == 5 or user.access == 6 else False,
                                                                   'logged_access' : self.Session['access'],
                                                                   'objects_count' : objects_count,
                                                                   'objects_list' : objects_list,
                                                                   'twitt'      : twitt,
                                                                   'lj'      : user.livejournal.encode("utf8") if user.livejournal else False,
                                                                   'date' : user.date if user.date else False,
                                                                   'user_about' : user.about.encode("utf8") if user.about else False, 
                                                                   })

        self.drawPage("Информация о пользователе "+user.name.encode("utf8")+" "+user.surname.encode("utf8"))
    
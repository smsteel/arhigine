# -*- coding: UTF-8 -*-﻿﻿
from event_handler import EventHandler
from google.appengine.ext import db

class EventsMy(EventHandler):
    """ guess who """
    
    url_handler = '/events/my/?'
    
    def get(self):
        """ Show all msg captions """
        self.checkSession(self.request.headers.get('Cookie'))
        self.insertMenu()
        self.insertTemplate('tpl_events_menu.html')
        self.insertContent("<h1>Вы создали события:</h1><br>")
        self.event = db.GqlQuery("SELECT * FROM DBEvent where userid = :userid",
                                 userid = self.Session['userid'], today=db.datetime.date.today())
        EventHandler.get(self)
        self.drawPage()

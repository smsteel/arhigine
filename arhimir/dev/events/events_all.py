# -*- coding: UTF-8 -*-﻿﻿
from event_handler import EventHandler
from google.appengine.ext import db

class EventsAll(EventHandler):
    """ guess who """
    
    url_handler = '/events/?'
    
    def get(self):
        """ Show all msg captions """
        self.checkSession(self.request.headers.get('Cookie'), False)
        self.insertMenu()
        self.insertTemplate('tpl_events_menu.html')
        self.event = db.GqlQuery("SELECT * FROM DBEvent where date >= :today", today = db.datetime.date.today())
        EventHandler.get(self)
        
        self.drawPage()
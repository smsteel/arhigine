#coding: UTF-8
from event_handler import EventHandler
from google.appengine.ext import db

class EventsByCat(EventHandler):
    """ guess who """
    
    url_handler = '/events/cat/.*'
    
    def get(self):
        """ Show all msg captions """
        self.checkSession(self.request.headers.get('Cookie'), False)
        self.insertMenu()
        self.insertTemplate('tpl_events_menu.html')
        catid = int(self.get_url_part(1))
        self.event = db.GqlQuery("SELECT * FROM DBEvent where catid = :cid",
                                 #today = db.datetime.date.today(),
                                 cid = catid).fetch(10)
        super(EventsByCat, self).get()
        self.drawPage()

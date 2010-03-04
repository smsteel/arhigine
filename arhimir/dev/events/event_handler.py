# -*- coding: UTF-8 -*-﻿﻿
from google.appengine.ext import db
from output_class import OutputClass
from db_entities.event_categories import DBEventCat

class EventHandler(OutputClass):
    """ guess who """
    def get(self):
        """ Show all msg captions """
        #"SELECT * FROM DBEvent"
        self.insertContent("<hr>&nbsp;&nbsp;&nbsp;Грядущие события:<br>")
        event = self.event #db.GqlQuery(self.query)   
        eventlist=''
        #self.checkSession(self.request.headers.get('Cookie'), False)
        found_events = False
        
        ec = DBEventCat()
        cats = ec.get_categories()
        
        for this_event in event:
            try:
                if not found_events: found_events = True
                if self.Session['access'] >= this_event.access or int(self.Session['userid']) == int(this_event.userid) or this_event.access <= 0:
                    eventlist += '<a href="/event/'+str(this_event.key().id())+'">'+this_event.name.encode("utf8")+'</a>'
                users = db.GqlQuery("SELECT * FROM DBEventAnketa WHERE eventid = :eventid",
                                    eventid = this_event.key().id())
                if self.Session['access'] >= 8 or int(self.Session['userid']) == int(this_event.userid): 
                    eventlist += '&nbsp;[ <i><a href="/event/info/' + str(this_event.key().id()) + '">Участников зарегистрировано: ' + str(users.count()) + '</i></a> ]<br>'
                elif self.Session['access'] >= this_event.access:
                    eventlist += '&nbsp;[ <i>Участников зарегистрировано: ' + str(users.count()) + '</i> ]<br>'
            except: continue
        if found_events:
            self.insertTemplate('tpl_event_add.html', { 'eventlist': eventlist, 'cats' : cats })
        else:
            self.insertContent("&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Пока мероприятий не запланировано!")
        self.insertContent("<hr>&nbsp;&nbsp;&nbsp;Недавно прошедшие события:<br>")
        
        eventlist = ''
        events = db.GqlQuery("SELECT * FROM DBEvent where date<:today order by date desc limit 10", today = db.datetime.date.today())
        for this_event in events:
            if self.Session['access'] >= this_event.access or int(self.Session['userid']) == int(this_event.userid):
                eventlist += '<a href="/event/'+str(this_event.key().id())+'">'+this_event.name.encode("utf8")+'</a>'
            users = db.GqlQuery("SELECT * FROM DBEventAnketa WHERE eventid = :eventid",
                                eventid = this_event.key().id())
            if self.Session['access'] >= 8 or int(self.Session['userid']) == int(this_event.userid): 
                eventlist += '&nbsp;[ <i><a href="/event/info/' + str(this_event.key().id()) + '">Участников зарегестрировано: ' + str(users.count()) + '</i></a> ]<br>'
            elif self.Session['access'] >= this_event.access:
                eventlist += '&nbsp;[ <i>Участников зарегистрировано: ' + str(users.count()) + '</i> ]<br>'
        self.insertTemplate('tpl_event_add.html', { 'eventlist': eventlist })

        
        #self.drawPage()
        
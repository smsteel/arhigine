# -*- coding: UTF-8 -*-﻿﻿
from google.appengine.ext import db
from output_class import OutputClass #@UnresolvedImport
from db_entities.event import DBEvent
from db_entities.event_categories import DBEventCat
from db_entities.event_picture import DBEventPicture
from google.appengine.api import images

class AdminEventHandler(OutputClass):
    """ guess who """
    
    url_handler = '/admin/event/?'
    def get(self):

        """ Show all msg captions """
        self.checkSession(self.request.headers.get('Cookie'))
        event = db.GqlQuery("SELECT * FROM DBEvent")
        eventlist=''
        self.insertMenu()
        ec = DBEventCat()
        cats = ec.get_categories()
        for this_event in event:
            if self.checkAccess('eventedit'):
                if self.Session['access'] >= this_event.access or int(self.Session['userid']) == int(this_event.userid):
                    eventlist += '<a href="/admin/event/'+str(this_event.key().id())+'">'+this_event.name+'</a><br>'
        if self.checkAccess('eventadd'):
            access = ''
            for an in self.accessNames:
                access += "<option value=" + str(an['access']) + ">" + str(an['name']) + "</option>\n"
            self.insertTemplate('tpl_event_add.html', { 'caption': 'Добавить событие:', 
                                                                    'access': access, 
                                                                    'eventlist': eventlist,
                                                                    'admin' : True, 
                                                                    'cats' : cats,
                                                                    'editor': self.insertFckEdit('descr', ToolbarSet = 'Admin'), })
        self.drawPage()
        
    def post(self):
        """ Write bullshit to DB """
        self.checkSession(self.request.headers.get('Cookie'))
        if not self.checkAccess('eventadd'): 
            self.insertMenu()
            self.insertContent('У вас нет прав на добавление события')
        else:
            event = DBEvent()
            event.name = self.request.get('name')
            event.minidescr = self.request.get('minidescr')[:1024]
            event.descr = self.request.get('descr')
            
            event.date = db.datetime.date.today()
            day = int(self.request.get('day'))
            month = int(self.request.get('month'))
            year = int(self.request.get('year'))
            if day and month and year:
                event.date = db.datetime.date(year,month,day)
                        
            event.time = self.request.get('time')
            event.access = int(self.request.get('access'))
            event.owner = self.request.get('owner')
            event.place = self.request.get('place')
            event.userid = self.Session['userid']
            event.catid = int(self.request.get('cat'))
            event.put()
            self.insertMenu()
            self.insertContent('Событие добавлено')
            dbevents = db.GqlQuery("SELECT * FROM DBEvent WHERE name = :name", name = event.name)
            eventid = dbevents.fetch(1)[0].key().id()
            data = self.request.get("pic")
            if data:
                try:
                    dbQuery = DBEventPicture.gql("WHERE eventid = :dbeventid", 
                                            dbeventid = int(eventid))
                    pics = dbQuery.fetch(1)
                    pic = pics[0]
                    avatar = images.resize(data, 400, 400)
                    pic.image = db.Blob(avatar)
                    pic.put()
                except:
                    pict = DBEventPicture()
                    avatar = images.resize(data, 400, 400)
                    pict.image = db.Blob(avatar)
                    pict.eventid = int(eventid)
                    pict.put()
        self.drawPage()

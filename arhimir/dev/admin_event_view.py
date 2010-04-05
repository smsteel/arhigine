#coding: UTF-8
from google.appengine.ext import db
from output_class import OutputClass
from db_entities.event import DBEvent
from db_entities.event_picture import DBEventPicture
from google.appengine.api import images
from db_entities.event_categories import DBEventCat

class AdminEventView(OutputClass):
    """ guess who """
    
    url_handler = '/admin/event/.*'
    
    def get(self):
        """ Show all msg captions """
        self.checkSession(self.request.headers.get('Cookie'))
        self.insertMenu()
        temp_uri = self.request.uri
        uri = temp_uri.split('/')
        event_id = int(uri[-1])
        event = DBEvent.get_by_id(event_id)
        if self.Session['access'] >= event.access or int(self.Session['userid']) == int(event.userid):
            access = ''
            for an in self.accessNames:
                access += "<option "
                try:
                    if int(event.access) == an['access']:
                        access += "selected "
                except:
                    pass
                access += "value=" + str(an['access']) + ">" + str(an['name']) + "</option>\n"
            ec = DBEventCat()
            cats = ec.get_categories()
            self.insertTemplate('tpl_event_add.html', { 'caption' : 'Изменить событие', 
                                                                    'name' : event.name.encode("utf8") ,
                                                                    'admin' : True, 
                                                                    'day' : str(event.date.day), # event.date.encode("utf8") if event.date else ''
                                                                    'month' : str(event.date.month),
                                                                    'year' : str(event.date.year),
                                                                    'time' : event.time.encode("utf8") if event.time else '',
                                                                    'place' : event.place.encode("utf8") if event.place else '',
                                                                    'owner' : event.owner.encode("utf8") if event.owner else '',
                                                                    'access' : access,
                                                                    'cats' : cats,
                                                                    'catid' : event.catid,
                                                                    'editor': self.insertFckEdit('descr', event.descr.encode("utf8"), 'Admin'), })
        else:
            self.insertContent('У вас нет прав на изменение этого события')
        self.drawPage()
        
    def post(self):
        self.checkSession(self.request.headers.get('Cookie'))
        self.insertMenu()
        temp_uri = self.request.uri
        uri = temp_uri.split('/')
        event_id = int(uri[-1])
        event = DBEvent.get_by_id(event_id)
        data = self.request.get("pic")
        if self.checkAccess('eventedit'):
            if data:
                try:
                    dbQuery = DBEventPicture.gql("WHERE eventid = :dbeventid", 
                                            dbeventid = int(event_id))
                    pics = dbQuery.fetch(1)
                    pic = pics[0]
                    avatar = images.resize(data, 400, 400)
                    pic.image = db.Blob(avatar)
                    pic.put()
                except:
                    pict = DBEventPicture()
                    avatar = images.resize(data, 400, 400)
                    pict.image = db.Blob(avatar)
                    pict.eventid = int(event_id)
                    pict.put()
                    
            if self.Session['access'] >= event.access or int(self.Session['userid']) == int(event.userid): 
                event.name = self.request.get('name')
                event.descr = self.request.get('descr')
                day = int(self.request.get('day'))
                month = int(self.request.get('month'))
                year = int(self.request.get('year'))
                event.date = db.datetime.date(year,month,day)
                event.time = self.request.get('time')
                event.place = self.request.get('place')
                event.access = int(self.request.get('access'))
                event.owner = self.request.get('owner')
                event.put()
                self.insertContent('Данные успешно изменены')
            else:
                self.insertContent('У вас нет прав на изменение этого события')
        else:
            self.insertContent('У вас нет прав на изменение этого события')
        self.drawPage()

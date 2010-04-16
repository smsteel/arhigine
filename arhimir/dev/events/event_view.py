#coding: UTF-8
from output_class import OutputClass
from db_entities.event import DBEvent
from db_entities.counter import DBCounter
from google.appengine.ext.webapp import template
import urllib
from google.appengine.ext import db

class EventView(OutputClass):
    """ guess who """
    
    url_handler = '/event/.*'
    
    def get(self):
        """ Show all msg captions """
        #self.checkSession(self.request.headers.get('Cookie'))
        
        # getting event_id
        event_id = 0
        try:
            event_id = int(self.request.uri.split('/')[-1])
        except:
            self.redirect('/page_not_found')
        
#        # geting pic
#        pic = db.GqlQuery("SELECT * FROM EventPicture where eventid = :eventid",
#                                  eventid = event_id)
        event = DBEvent.get_by_id(event_id)
        if not event:
            self.redirect('/page_not_found')
        self.checkSession(self.request.headers.get('Cookie'), False)
        self.insertMenu()
        if self.Session['access'] >= event.access or int(self.Session['userid']) == int(event.userid) or int(event.access) <= 0:
            tpl_cust = template.Template ("""<a href=\"" + self.paramByName("url") + "/event/reg/{{ event_id }}">Регистрация на мероприятие</a>""")
            self.insertTemplate('tpl_event_view.html', { 'event_id' : str(event_id),
                                                                     'event_name' : event.name.encode("utf8"),
                                                                     'event_descr' : event.descr.encode("utf8"),
                                                                     'date' : str(event.date) if event.date else '',
                                                                     'time' : event.time.encode("utf8") if event.time else '',
                                                                     'place' : event.place.encode("utf8") if event.place else '',
                                                                     'owner' : event.owner.encode("utf8") if event.owner else '',
                                                                     'register' : tpl_cust.render(template.Context({ 'event_id' : str(event_id), 
                                                                                                                               'counter'   : ""})) if event.date >= db.datetime.date.today() else False
                                                                     })

            
            self.insertComments(event.key())
        else:
            self.insertContent("У вас нет прав на просмотр этого события")
        self.drawPage(event.name.encode("utf8"))
        
    def post(self):
        self.checkSession(self.request.headers.get('Cookie'), False)
        temp_uri = self.request.uri
        uri = temp_uri.split('/')
        event_id = int(uri[-1])
        site4check = urllib.urlopen(self.request.get('verificator'))
        content = site4check.read()
        site4check.close()
        if content.find(self.insertTemplate('tpl_counter.html', { 'userid' : str(self.Session['userid']),
                                                                'event_id' : str(event_id), })) >= 0:
            counter = DBCounter()
            counter.userid = self.Session['userid']
            counter.eventid = event_id
            counter.url = self.request.get('verificator')
            counter.put()
        
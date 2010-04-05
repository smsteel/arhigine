#coding: UTF-8
from output_class import OutputClass
from google.appengine.ext import db
from db_entities.event import DBEvent

class EventsSigned(OutputClass):
    """ guess who """
    
    url_handler = '/events/signed/?'
    
    def get(self):
        self.checkSession(self.request.headers.get('Cookie'))
        """ Show all msg captions """
        signed_events = db.GqlQuery("SELECT * FROM DBEventAnketa WHERE userid=:userid ORDER BY eventid",
                                    userid = self.Session['userid'])
#        signed_events = db.Query(DBEventAnketa)
#        signed_events.filter('userid =', self.Session['userid'])
#        signed_events.order('eventid')
        self.insertMenu()
        self.insertTemplate('tpl_events_menu.html')
        self.insertContent('<h1>Вы подписались на события:</h1>')
        #found_events = False
        eventlist = ''
        for signed_event in signed_events:
            #if not found_events: found_events = True
            try:
                this_event = DBEvent.get_by_id(int(signed_event.eventid))
                
                eventlist += '<a href="/event/'+str(this_event.key().id())+'">'+this_event.name.encode("utf8")+'</a>'
                users = db.GqlQuery("SELECT * FROM DBEventAnketa WHERE eventid = :eventid",
                                    eventid = this_event.key().id())
                eventlist += '&nbsp;[ <i><a href="/event/info/' + str(this_event.key().id()) + '">Участников зарегистрировано: ' + str(users.count()) + '</i></a> ]<br>'
            except:
                continue
        if eventlist != '':
            self.insertTemplate('tpl_event_add.html', { 'eventlist': eventlist })
        else:
            self.insertContent("Нет ни одного события, на которое вы подписались!")
        self.drawPage()

        #EventHandler.get(self)

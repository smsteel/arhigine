#coding: UTF-8
from google.appengine.ext import db
from output_class import OutputClass
from db_entities.event import DBEvent
from db_entities.user import DBUser

class EventInfo(OutputClass):
    
    url_handler = '/event/info/.*'
    access = 8
    
    def get(self):
        eventid = self.request.uri.split('/')[-1]
        event = DBEvent.get_by_id(int(eventid))
        if not super(EventInfo, self).get(event.userid): return
        users = db.GqlQuery("SELECT * FROM DBEventAnketa WHERE eventid = :eventid",
                            eventid = event.key().id())
        user_list = []
        for user in users:
            user_list.append({
                               'id' : int(user.userid),
                               'login' : DBUser().get_login_by_id(int(user.userid)),
                               'name' : user.name.encode("utf8"),
                               'surname' : user.surname.encode("utf8"),
                               'phone' : user.phone.encode("utf8"),
                            })
        self.insertMenu()
        self.insertTemplate("tpl_event_info.html", {
                                                     'user_list' : user_list,
                                                     'event' : { 
                                                                 'name' : event.name.encode("utf8"),
                                                                 'id'   : event.key().id(),
                                                               },
                                                   })
        self.drawPage(event.name.encode("utf8"))

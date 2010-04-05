#coding: UTF-8
from output_class import OutputClass
from db_entities.event import DBEvent
from db_entities.user import DBUser
from db_entities.event_anketa import DBEventAnketa
from message.handler import Handler

class EventMailFeed(OutputClass):
    
    url_handler = '/admin/event_msg/.+'
    access = 8
    
    def get(self):
        id = int(self.request.uri.split('/')[-1])
        try: 
            event = DBEvent.get_by_id(id)
        except:
            self.showMessage("Событие на найдено!")
            return
        if not super(EventMailFeed, self).get(event.userid): return
        self.insertMenu()
        self.insertTemplate("tpl_message.html", { 'ckeditor' : self.insertFckEdit("content") })
        self.drawPage()
        
    def post(self):
        #@todo: Test it on GAE
        id = int(self.request.uri.split('/')[-1])
        try: 
            self.event = DBEvent.get_by_id(id)
        except:
            self.showMessage("Событие на найдено!")
            return
        if not super(EventMailFeed, self).get(self.event.userid): return
        message_handler = Handler()
        anketas = DBEventAnketa.gql("where eventid = :eventid", eventid = id)
        user_list = []
        for anketa in anketas:
            user_list.append(DBUser.get_by_id(anketa.userid))
        message_handler.send(self.Session['user_key'], user_list, ("""Новая информация о событии %s""" % self.event.name.encode("utf-8")).decode("utf-8"), self.request.get('content'))
        #sender.send_msg_mass(self.event.userid, recipients, self.request.get('content'), db.Text("Новая информация о событии " + self.event.name.encode("utf8"), "utf_8"))
        self.showMessage("Готово")

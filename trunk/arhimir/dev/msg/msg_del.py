# -*- coding: UTF-8 -*-

from msg_handler import MSGHandler
from db_entities.message_recipients import DBMSGRecipients
from google.appengine.ext import db

class MSGDel(MSGHandler):
    """ guess who """
    
    url_handler = '/msg/del/.*'
    
    def get(self):
        self.checkSession(self.request.headers.get('Cookie'))
        id = int(self.request.uri.split('/')[-1])
        userid = int(self.Session['userid'])
        msg_r = DBMSGRecipients.get_by_id(id)
        
        if int(msg_r.message.owner) == userid:
            msg_r.message.show_to_owner = False
            msg_r.message.put()
            self.showMessage("Сообщение удалено")
        elif int(msg_r.recipient) == userid:
            db.delete(msg_r)
            self.showMessage("Сообщение удалено")
        else:
            self.showMessage("Ошибка какая-то!")
                        
from db_entities.message.message import Message
from db_entities.message.rcp_list import Rcp_list
from sendmail.post_office import PostOffice
from google.appengine.ext import db

class Handler():
    
    def send(self, owner, rcp, title, body): #rcp must be a list!
        new_msg = Message()
        new_msg.owner = owner
        new_msg.title = title
        new_msg.body = body
        message = new_msg.put()
        
        for r in rcp:
            msg_r = Rcp_list()
            msg_r.rcp = r
            msg_r.message = message
            msg_r.put()
            PostOffice().append_to_queue(r, title, body)
            
    def get_incoming(self, user):
        rcp_list = Rcp_list.gql("where rcp = :rcp", rcp = user)
        messages = []
        for entity in rcp_list:
            if entity.deleted: continue
            messages.append(entity.message)
        return self.__get_letters(messages)
    
    def get_outgoing(self, user):
        messages = Message.gql("where owner = :owner and deleted = :is_deleted", owner = user, is_deleted = False)
        return self.__get_letters(messages)
    
    def __get_letters(self, messages):
        formalized_messages = []
        for message in messages:
            owner = { 'login' : message.owner.login }
            rcp = []
            r_read = False
            rcp_list = Rcp_list.gql("where message = :message", message = message)
            for r in rcp_list:
                rcp.append({'login': r.rcp.login})
                r_read = r.read
            title = message.title
            o_read = message.read
            datetime = message.datetime
            formalized_messages.append({'key' : message.key(), 'r_read' : r_read, 'o_read' : o_read, 'owner':owner, 'rcp':rcp[:5], 'title':title, 'datetime': datetime})
            formalized_messages.sort(key=lambda k: k['datetime'])
        return formalized_messages
            
    def delete(self, messages, user):
        messages_ = db.get(messages)
        for message in messages_:
            if message.owner == user:
                message.deleted = True
                message.put()
            else:
                rcp = Rcp_list.gql("where message = :message and rcp = :rcp", message = message, rcp = user)[0]
                rcp.deleted = True
                rcp.put()
                
                
                
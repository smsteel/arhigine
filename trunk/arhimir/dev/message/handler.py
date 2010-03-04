from db_entities.message.message import Message
from db_entities.message.rcp_list import Rcp_list
from sendmail.post_office import PostOffice

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
            
            
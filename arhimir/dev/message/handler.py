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
            
    def get_incoming(self, user):
        rcp_list = Rcp_list.gql("where rcp = :rcp", rcp = user)
        messages = []
        for entity in rcp_list:
            messages.append(entity.message)
        return self.__get_letters(messages)
    
    def get_outgoing(self, user):
        messages = Message.gql("select __key__ where owner = :owner", owner = user)
        return self.__get_letters(messages)
    
    def __get_letters(self, messages):
        formalized_messages = []
        for message in messages:
            owner = message.owner.login
            rcp = []
            rcp_list = Rcp_list.gql("where message = :message", message = message)
            for r in rcp_list:
                rcp.append()
            title = message.title
            show_to_owner = message.show_to_owner
            show_to_rcp = message.show_to_rcp
            datetime = message.datetime
            formalized_messages.append({'owner':owner, 'rcp':rcp, 'title':title, 'show_to_owner': show_to_owner, 'show_to_rcp': show_to_rcp, 'datetime': datetime})
        return formalized_messages
            
            
            
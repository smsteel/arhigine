# -*- coding: UTF-8 -*-

from db_entities.message.message import Message
from db_entities.message.rcp_list import Rcp_list
from sendmail.post_office import PostOffice
from google.appengine.ext import db
from tools.tag_processor import tag_processor

class Handler():
    
    def send(self, owner, rcp, title, body): #rcp must be a list!
        new_msg = Message()
        new_msg.owner = owner
        new_msg.title = tag_processor().mask_tags(title)
        new_msg.body = tag_processor().prepare(body)
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
    
    def get_letter(self, letter, user):
        letter_ = db.get(letter)
        rcp = False
        try:
            rcp = Rcp_list.gql("where message = :letter and rcp = :user", letter = db.Key(letter), user = user)[0]
        except: pass
        if letter_.owner.key() == user or rcp:
            rcp.read = True
            rcp.put()
            return letter_

            
    def delete(self, messages, user):
        messages_ = db.get(messages)
        for message in messages_:
            if message.owner == user:
                message.deleted = True
                message.read = True
                message.put()
            else:
                rcp = Rcp_list.gql("where message = :message and rcp = :rcp", message = message, rcp = user)[0]
                rcp.deleted = True
                rcp.read = True
                rcp.put()
                
    def has_unread_msg(self, user):
        try:
            return Rcp_list.gql("where rcp = :rcp and read = :read", rcp = user, read = False).count(1)
        except:
            return False
# -*- coding: UTF-8 -*-

from sendmail.post_office import PostOffice
from db_entities.user import DBUser

class MassSender():
    
    def send_all(self, subject, body):
        all = DBUser.all()
        self._send(all, subject, body)
    
    def send_arch(self, subject, body):
        arhs = DBUser.gql("where access = 6")
        self._send(arhs, subject, body)
    
    def send_admin(self, subject, body):
        admins = DBUser.gql("where access >= 8")
        self._send(admins, subject, body)
    
    def _send(self, users, subject, body):
        for user in users:
            PostOffice().append_to_queue(user.key(), subject, body)
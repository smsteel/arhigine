# -*- coding: UTF-8 -*-

from db_entities.user import DBUser
from output_class import OutputClass
from google.appengine.ext import db
from db_entities.news import DBNews
from db_entities.event import DBEvent

class fix(OutputClass):
    
#    url_handler = '/fix'
    
    def get(self):
        
        news = DBEvent.all()
        for new in news:
            new.author = DBUser.get_by_id(new.userid)
            new.put()
       
#        users_ = [7051,12041,13015,13016,14001,15015,15033,15040,15056,15069,16011,16018,16031,19003,19008]
#        users = DBUser.get_by_id(users_)
#        for user in users:
#            user.date = db.datetime.datetime.today()
#            user.put()
# -*- coding: UTF-8 -*-

from db_entities.user import DBUser
from output_class import OutputClass
from google.appengine.ext import db
from db_entities.news import DBNews
from db_entities.event import DBEvent
from db_entities.photo_tags import DBPhotoTags
from db_entities.album import DBAlbum

class fix(OutputClass):
    
    url_handler = '/fix/.*'
    
    def get(self):
        
        try:
            i = int(self.get_url_part(1))
        except:
            i = 0
        
        news = DBAlbum.all()[i:i+200]
        for new in news:
            new.author = DBUser.get_by_id(new.userid)
            new.put()
       

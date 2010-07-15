# coding: utf-8

from output_class import OutputClass
from db_entities.photo_tags import DBPhotoTags
from db_entities.photo import DBPhoto
from db_entities.user import DBUser
from db_entities.tag.tag import TagsList
from google.appengine.ext import db

class TagCoverter(OutputClass):
    
    url_handler = '/tag_convert/?'
    
    def get(self):
        old_tags = DBPhotoTags.gql('where fixed = :fixed', fixed = False)
        for tag_string in old_tags:
            tags = tag_string.tags.split(',')
            imageid = tag_string.imageid
            
            key = DBPhoto.get_by_id(imageid).key()
           
            user = DBUser.gql("where login='spe'")[0]
            new_tag = TagsList()
            new_tag.obj = db.Key(str(key))
            new_tag.tags = tags
            new_tag.user = user
            new_tag.put()
            
            tag_string.fixed = True
            tag_string.put()
            self.response.out.write('ok')
        self.response.out.write('done')
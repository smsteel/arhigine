# coding: utf-8

from output_class import OutputClass
from db_entities.photo_tags import DBPhotoTags
from db_entities.photo import DBPhoto
from db_entities.user import DBUser
from db_entities.tag.tag import TagsList

class TagCoverter(OutputClass):
    
    url_handler = '/tag_convert/?'
    
    def get(self):
        old_tags = DBPhotoTags.gql("limit 10")
        for tag_string in old_tags:
            tags = tag_string.split(',')
            imageid = tag_string.imageid
            
            key = DBPhoto.get_by_id(imageid)
            
            user = DBUser.gql("where login='spe'")[0]
            new_tag = TagsList()
            new_tag.entity = key
            new_tag.tags = tags
            new_tag.user = user
            new_tag.put()
            
        self.response.out.write('ok')
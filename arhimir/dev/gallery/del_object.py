# -*- coding: UTF-8 -*-
from output_class import OutputClass
from db_entities.gallery_object import DBGalleryObject
from db_entities.album import DBAlbum
from db_entities.photo import DBPhoto
from db_entities.photo_tags import DBPhotoTags
from google.appengine.ext import db

class DelObject(OutputClass):
    
    url_handler = '/admin/deleteobject/.*'
    access = 8
    
    def get(self):
        id = int(self.request.uri.split('/')[-1])
        object = DBGalleryObject.get_by_id(id)
        if not super(DelObject, self).get(object.userid): return
        albums = DBAlbum.gql("WHERE objectid = :objectid", objectid = id)
        for album in albums:
            photos = DBPhoto.gql("WHERE albumid = :albumid", albumid = int(album.key().id()))
            for photo in photos:
                try:
                    tags = DBPhotoTags.gql("where imageid = :imageid", imageid = int(photo.key().id()))
                    db.delete(tags)
                except: pass 
            db.delete(photos)
        db.delete(albums)
        db.delete(object)
        self.showMessage("Объект успешно удален")

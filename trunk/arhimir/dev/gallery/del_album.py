from db_entities.album import DBAlbum
from db_entities.photo import DBPhoto
from db_entities.photo_tags import DBPhotoTags
from output_class import OutputClass
from google.appengine.ext import db

class DelAlbum(OutputClass):

    url_handler = '/admin/deletealbum/.*'
    access = 8
        
    def get(self):
        id = int(self.request.uri.split('/')[-1])
        album = DBAlbum.get_by_id(id)
        if not super(DelAlbum, self).get(album.userid): return
        
        
        
        album = DBAlbum.get_by_id(id)
        db.delete(album)
        
        photos = DBPhoto.gql("where albumid = :albumid", albumid=id)
        for photo in photos:
            try:
                tags = DBPhotoTags.gql("where imageid = :imageid", imageid = int(photo.key().id()))
                db.delete(tags)
            except: pass
        db.delete(photos)
        self.redirect('/msgbox/albumdeleted')
        
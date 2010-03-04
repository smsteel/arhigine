from db_entities.album import DBAlbum
from db_entities.photo import DBPhoto
from db_entities.photo_tags import DBPhotoTags
from output_class import OutputClass
from google.appengine.ext import db

class DelPhoto(OutputClass):

    url_handler = '/del_photo/.*'
    access = 8
        
    def get(self):
        id = int(self.request.uri.split('/')[-1])
        photo = DBPhoto.get_by_id(id)
        albom_ppc = DBAlbum.get_by_id(int(photo.albumid))
        
        if not super(DelPhoto, self).get(albom_ppc.userid): return
        
        db.delete(photo)
            
        tag = DBPhotoTags.gql("where imageid = :imageid", imageid=id)
        db.delete(tag)
            
        self.insertContent("Удалено успешно!")
        self.drawPage()
        self.redirect("/album/%s" % str(albom_ppc.key().id()))
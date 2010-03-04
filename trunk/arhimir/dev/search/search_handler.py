from google.appengine.ext import db
from output_class import OutputClass
from db_entities.photo_tags import DBPhotoTags
from db_entities.photo import DBPhoto

class SearchHandler(OutputClass):
    """ guess who """
    
    url_handler = '/search/?'
    
    def post(self):
        self.checkSession(self.request.headers.get('Cookie'), False)
        self.insertMenu()
        query = self.request.get('find')
        self.insertContent("<div style='width: 100%;'><div style='padding: 10px;'>Поиск по запросу: "+query.encode("utf8")+"<hr>")

        tphotos = db.Query(DBPhotoTags)
          
        any_found = False
        for tphoto in tphotos:
            try:
                if query in tphoto.tags.split(","):
                    any_found = True
                    photo = DBPhoto.get_by_id(int(tphoto.imageid))
                    self.insertContent("""<div style='float: left; margin: 5px;'><a style="border-width: 0px;" href="/album/%s">""" % str(photo.albumid))
                    self.insertContent("<img style='border-width:0px;' src='/picture/3/" + str(photo.key().id()) + "'></img>")
                    self.insertContent("</a></div>")
            except: pass
        if not any_found: self.insertContent("К сожалению, ничего не найдено по вашему запросу")
        self.insertContent("</div></div>")
        self.drawPage()
        

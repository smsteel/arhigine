from db_entities.album import DBAlbum
from output_class import OutputClass
from google.appengine.ext import db

class AdminAlbumList(OutputClass):
    
    url_handler = '/admin/albumlist/?'
    access = 8
    
    def get(self):
        if super(AdminAlbumList, self).get():
            self.insertMenu()
            albums = db.Query(DBAlbum)
            for album in albums:
                self.insertContent("""<a href=\"/album/""" + str(album.key().id()) + """\">""" + str(album.key().id()) + """</a><br>""")
            self.drawPage()

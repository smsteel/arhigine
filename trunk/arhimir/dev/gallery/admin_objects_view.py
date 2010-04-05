#coding: UTF-8
from google.appengine.ext import db
from db_entities.gallery_object import DBGalleryObject
from db_entities.album import DBAlbum
from admin_object_add import AdminObjectAdd

class AdminObjectsView(AdminObjectAdd):
    
    url_handler = '/admin/objects/.*'
    
    def get(self):
        self.checkSession(self.request.headers.get('Cookie'))
        if self.Session['access'] > 4:
            self.insertMenu()
            id = int(self.request.uri.split('/')[-1])
            object = DBGalleryObject.get_by_id(id)
            self.insertContent("""<div style="padding: 10px;">Связанные фотоальбомы:""")
            albums = db.Query(DBAlbum)
            albums.filter("objectid =", id)
            for album in albums:
                self.insertContent("""<li><a href='/album/""" + str(album.key().id()) + """'>""" + album.name.encode("utf8") + """</a></li>""")
                
            self.insertContent("""<div class="form"><a href="/admin/album/add/""" + str(id) + """\">Добавить альбом</a></div>""")
            self.insertTemplate("tpl_object_add.html", { 'editor'           : self.insertFckEdit("descr", object.description.encode("utf8"), ToolbarSet = "Admin"),
                                                         'name'             : object.name.encode("utf8"),
                                                         'button'           : 'Изменить',
                                                         'caption'          : 'Изменение',
                                                         'id'               : str(id), 
                                                         'userid'           : str(object.userid)
                                                         })
        else:
            self.insertContent("У вас нет прав на выполнение этого действия")
        self.drawPage()

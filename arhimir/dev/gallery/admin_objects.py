#coding: utf-8
from google.appengine.ext import db
from admin_object_add import AdminObjectAdd
from db_entities.gallery_object import DBGalleryObject

class AdminObjects(AdminObjectAdd):

    url_handler = '/admin/objects/?'

    def get(self):
        self.checkSession(self.request.headers.get('Cookie'))
        if self.Session['access'] > 4:
            self.insertMenu()
            objects = db.Query(DBGalleryObject)
            if self.Session['access'] < 8:
                objects.filter("userid =", self.Session['userid'])
            self.insertContent("<div style='padding: 10px;'>"
                               """<div style='padding: 5px;'><input onclick="window.location = '/admin/objects/add/';" type='submit' value='Добавить объект'></div>Объекты:""")
            for object in objects:
                self.insertContent("""<li style="float: left;"><a href="/admin/objects/""" + str(object.key().id()) + """\">""" + object.name.encode("utf8") + """
                                        <br><img style="border: 0;" src="/picture/130/crop/0/""" + str(object.key().id()) + """" /></a></li>""")
            self.insertContent("</div>")
            
        else:
            self.insertContent("У вас нет прав на выполнение этого действия")
        self.drawPage()

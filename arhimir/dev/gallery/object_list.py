#coding: UTF-8
from google.appengine.ext import db
from output_class import OutputClass
from db_entities.gallery_object import DBGalleryObject

class ObjectList(OutputClass):

    url_handler = '/objects/?'
    access = 0

    def get(self):
        self.checkSession(self.request.headers.get('Cookie'))

        self.insertMenu()
        objects = db.Query(DBGalleryObject)
        #objects.filter("userid =", self.Session['userid'])
        self.insertContent("<div style='padding: 10px; width: 100%;'>"
                           """<div>Объекты:</div>""")
        for object in objects:
            self.insertContent('<div style="padding: 2 2 2 2; float: left;"><div style="text-align: center; padding-bottom: 2px;"><font style="font-size: 10px; text-decoration: none;">' + object.name.encode("utf8") + '</font></div><div style="background-opacity: 0.7; background-image: url(/images/objects_back.jpg); padding: 5px; float: left; border-style: solid; border-width: 1px; width: 300px; height: 300px;"><a href="/objects/' + str(object.key().id()) + '"><img style="border: 0;" src="/picture/crop/0/' + str(object.key().id()) + '"></img></a></div></div>')
        self.insertContent("</div>")
            
        self.drawPage("Список объектов")
        
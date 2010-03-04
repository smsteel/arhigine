from output_class import OutputClass
from db_entities.gallery_object import DBGalleryObject

class LastObjectsList(OutputClass):

    access = 0
    url_handler = '/last_objects/?'

    def get(self):
        if self.checkSession(self.request.headers.get('Cookie'), False):
            self.insertMenu()
            
        objects = DBGalleryObject.gql("order by date desc limit 50")
        #objects.filter("userid =", self.Session['userid'])
        self.insertContent("<div style='padding: 10px; width: 100%;'>"
                           """<div>Объекты:</div>""")
        for object in objects:
            self.insertContent('<div style="padding: 2 2 2 2; float: left;"><div style="text-align: center; padding-bottom: 2px;"></div><div style="background-opacity: 0.7; padding: 5px; float: left; border-style: solid; border-width: 1px; width: 128px; height: 128px;"><a href="/objects/' + str(object.key().id()) + '"><img alt="'+object.name.encode("utf8")+'" src="/picture/128/crop/0/' + str(object.key().id()) + '"></img></a></div></div>')
        self.insertContent("</div>")
            
        self.drawPage("Последние поступления")
        
#coding: UTF-8
from google.appengine.api import images
from output_class import OutputClass
from db_entities.gallery_object import DBGalleryObject
from google.appengine.ext import db

class AdminObjectAdd(OutputClass):

    url_handler = '/admin/objects/add/?'

    def get(self):
        self.checkSession(self.request.headers.get('Cookie'))
        self.insertMenu()
        if self.Session['access'] > 4:
            self.insertTemplate("tpl_object_add.html", { 'editor' : self.insertFckEdit("descr"),
                                                         'button' : 'Добавить',
                                                         'caption': 'Добавление', 
                                                         'isadmin' : True if self.Session['access'] > 7 else False,
                                                          })
        else:
            self.insertContent("У вас нет прав на выполнение этого действия")
        self.drawPage()
    
    def post(self):
        self.checkSession(self.request.headers.get('Cookie'))
        if self.Session['access'] > 4:
            if not self.request.get('name'):
                self.showMessage("Вы не указали имя объекта")
                return
            id = self.request.get('id')
            try: 
                self.object = DBGalleryObject.get_by_id(int(id))
                self.answer = "objectedittrue"
            except:
                self.object = DBGalleryObject()
                self.answer = "objectaddtrue"
            if self.request.get("login"):
                query = db.GqlQuery("SELECT * FROM DBUser WHERE login = :login", login = self.request.get("login"))
                if query.count() == 0: self.object.userid=self.Session['userid']
                for q in query:
                    self.object.userid = int(q.key().id())
            else:
                if self.request.get("userid"):
                    self.object.userid = int(self.request.get("userid"))
                else:
                    self.object.userid = self.Session['userid']
            self.object.name = self.request.get('name')
            self.object.description = self.request.get('descr')
            self.object.smalldescription = self.request.get('smalldescription')
            data = self.request.get('pic')
            if data:
                try:
                    image = images.resize(data, 300, 300)
                    self.object.image = db.Blob(image)
                except:
                    self.showMessage("Картинка объекта не должна быть размером больше, чем 1 Мб.")
                    return
            self.object.put()
            self.redirect('/msgbox/' + self.answer)
        else:
            self.insertContent("У вас нет прав на выполнение этого действия")
            self.drawPage()

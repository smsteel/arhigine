#coding: UTF-8
from db_entities.album import DBAlbum
from db_entities.photo import DBPhoto
from db_entities.photo_tags import DBPhotoTags
from output_class import OutputClass
from google.appengine.ext import db
from google.appengine.api import images

class EditPhoto(OutputClass):

    url_handler = '/edit_photo/.*'

    def get(self):
        
        self.checkSession(self.request.headers.get('Cookie'))
        self.insertMenu()
        
        id = int(self.request.uri.split('/')[-1])
        photo = DBPhoto.get_by_id(id)
        albom_ppc = DBAlbum.get_by_id(int(photo.albumid))
        
        if(self.Session['access'] >= 8 or self.Session['userid'] == int(albom_ppc.userid) ):
            
            tags = ""
            
            try:
                tags1 = DBPhotoTags.gql("where imageid = :imageid", imageid=id)
                for tag in tags1:
#                    self.insertContent("1")
                    tags = tag.tags.encode("utf8")
            except: pass
#            try:
#                tags = photo.tags.encode("utf8")
#            except: pass
            
            """ TODO: javascript it! """
            self.insertTemplate("tpl_edit_photo.html", { 'tags' : tags,
                                                                     'id' : id })
#            self.insertContent(""" 
#            <form method="post" enctype="multipart/form-data">
#                <input type="file" name="pic">
#                <br>
#                Key words<input type="text" name="tags" value="%s">
#                <br>
#                <input type="submit" value="OK">
#            </form> """ % tags)
#            self.insertContent('<br><br><a href="/del_photo/%s">Удалить навсегда!</a>' % str(id))
        else:
            self.insertContent("Плохие новости: Доступ запрещен!") 
        self.drawPage("Редактирование фото")
        
    def post(self):
        self.checkSession(self.request.headers.get('Cookie'))
        self.insertMenu()
        
        id = int(self.request.uri.split('/')[-1])
        photo = DBPhoto.get_by_id(id)
        albom_ppc = DBAlbum.get_by_id(int(photo.albumid))
        
        if(self.Session['access'] >= 8 or self.Session['userid'] == int(albom_ppc.userid) ):
            if self.request.get('pic'):
                image = images.Image(self.request.get('pic'))
                image_resized = images.Image(images.resize(image._image_data, width=130, output_encoding = images.JPEG)) if image.height >= image.width else images.Image(images.resize(image._image_data, height=130, output_encoding = images.JPEG))
                image_cropped = images.crop(image_resized._image_data, 0.0, 0.0, float(130)/float(image_resized.width), 1.0, images.JPEG) if image_resized.height == 130 else images.crop(image_resized._image_data, 0.0, 0.0, 1.0, float(130)/float(image_resized.height), images.JPEG)
                photo.image_small = db.Blob(image_cropped)
                if (image.width < 400 and image.height < 400) or image.width > 1024 or image.height > 768:
                    self.insertContent("Фотография не должна быть больше 1024x768 пикселей, но хотя бы одна сторона фотографии должна быть больше 400 пикселей")
                    self.drawPage()
                    return
                photo.image_big = db.Blob(image._image_data)
            photo.put()
            
            try:
                tags = DBPhotoTags.gql("where imageid = :imageid", imageid=id)
                if tags.count()==0: 1/0
                for tag in tags:
                    tag.tags = self.request.get('tags')
                    tag.put()
            except:
                tags = DBPhotoTags()
                tags.tags = self.request.get('tags')
                tags.imageid = id
                tags.put()
            
            self.insertContent("Изменено успешно!")
        self.drawPage()
        self.redirect("/album/%s" % str(albom_ppc.key().id()))
#coding: UTF-8
import hashlib, random
from db_entities.photo import DBPhoto
from db_entities.photo_tags import DBPhotoTags
from output_class import OutputClass
from google.appengine.ext import db
from google.appengine.api import images

class AddPhoto(OutputClass):
    
    url_handler = '/admin/addphoto/.*'
    access = 5
    
    def get(self):
        self.checkSession(self.request.headers.get('Cookie'))
        self.insertMenu()
        """ TODO: javascript it! """
        self.insertContent(""" 
        <form method="post" enctype="multipart/form-data">
            <input type="file" name="pic">
            <br>
            Key words<input type="text" name="tags">
            <br>
            <input type="submit" value="OK">
        </form> """)
        self.drawPage("Добавление фото")
        
    def post(self):
        id = int(self.request.uri.split('/')[-1])
        if self.request.get('pic'):
            photo = DBPhoto()
            image = images.Image(self.request.get('pic'))
            image_resized = images.Image(images.resize(image._image_data, width=130, output_encoding = images.JPEG)) if image.height >= image.width else images.Image(images.resize(image._image_data, height=130, output_encoding = images.JPEG))
            image_cropped = images.crop(image_resized._image_data, 0.0, 0.0, float(130)/float(image_resized.width), 1.0, images.JPEG) if image_resized.height == 130 else images.crop(image_resized._image_data, 0.0, 0.0, 1.0, float(130)/float(image_resized.height), images.JPEG)
            photo.image_small = db.Blob(image_cropped)
            if (image.width < 400 and image.height < 400) or image.width > 1024 or image.height > 768:
                self.insertContent("Фотография не должна быть больше 1024 пикселей в ширину и 768 пикселей в высоту, но хотя бы одна сторона фотографии должна быть больше 400 пикселей. При этом размер файла с фотографие должен быть не более 1мб.")
                self.drawPage()
                return
            photo.image_big = db.Blob(image._image_data)
            #photo.image_big = db.Blob(images.resize(self.request.get('pic'), 1024, 768))
            #photo.tags = self.request.get('tags')
            photo.albumid = id
            secret = str(hashlib.md5(str(random.random())).hexdigest())
            photo.comment = secret
            photo.put()
            photo_temp = DBPhoto.gql("where comment = :comment", comment = secret)
            tags = DBPhotoTags()
            tags.tags = self.request.get('tags')
            tags.imageid = int(photo_temp[0].key().id())
            tags.put()
        
        self.redirect("/album/%s" % str(id))

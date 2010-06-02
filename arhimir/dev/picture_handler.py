from google.appengine.ext import webapp
from google.appengine.ext import db
from db_entities.gallery_object import DBGalleryObject
from db_entities.news import DBNews
from db_entities.photo import DBPhoto
from tools.watermark import WaterMark
from google.appengine.api import images

class PictureHandler(webapp.RequestHandler):
    
    url_handler = '/picture/.*'
    
    __entities = { 0 : DBGalleryObject,
                   1 : "SELECT * FROM DBAvatara where userid = :queryid",
                   2 : DBNews,
                   3 : DBPhoto,
                   4 : DBPhoto, }
    
    def get(self):
        
        id = int(self.request.uri.split('/')[-1])
        
        entity = int(self.request.uri.split('/')[-2])
        
        dowatermark = True if str(self.request.uri.split('/')[-3]) == "watermark" else False
        docrop = True if str(self.request.uri.split('/')[-3]) == "crop" else False
        cropsize = int(self.request.uri.split('/')[-4]) if docrop else 100 
        watermark = WaterMark()
        
        try:
            self.query = self.__entities[entity].get_by_id(id)
        except:
            tquery = db.GqlQuery(self.__entities[entity], queryid = id)
            self.query = tquery.fetch(1)[0]
        if self.query:
            self.response.headers['Content-Type'] = 'image/jpeg'
            self.response.headers['Expires'] = "Thu,01 Jan 2020 00:00:01 GMT"
            self.response.headers['Cache-Control'] = "public"
            if entity == 3:
                image = watermark.insert(self.query.image_small) if dowatermark else self.query.image_small
                self.response.out.write(image)
            elif entity == 4:
                image = watermark.insert(self.query.image_big) if dowatermark else self.query.image_big
                self.response.out.write(image)
            else:
                image = images.Image(self.query.image)
                image_resized = images.Image(images.resize(image._image_data, width=cropsize, output_encoding = images.JPEG)) if image.height >= image.width else images.Image(images.resize(image._image_data, height=cropsize, output_encoding = images.JPEG))
                image_cropped = images.crop(image_resized._image_data, 0.0, 0.0, float(cropsize)/float(image_resized.width), 1.0, images.JPEG) if image_resized.height == cropsize else images.crop(image_resized._image_data, 0.0, 0.0, 1.0, float(cropsize)/float(image_resized.height), images.JPEG)
#                image = images.Image(images.resize(self.query.image, height=cropsize, output_encoding=images.JPEG))
#                if image.width > image.height:
#                    self.imagec = images.crop(image._image_data, 0.0, 0.0, float(cropsize)/float(image.width), 1.0, images.JPEG)
#                else: self.imagec = image._image_data
                self.response.out.write(image_cropped if docrop else self.query.image)

from google.appengine.api import images
from google.appengine.api import urlfetch
from db_entities.custom_field import DBCustomField

class WaterMark():
    
    __watermark_addr = DBCustomField().getByName("url_watermark") #"http://7.latest.ru-dev.appspot.com/images/watermark.png"

    def insert(self, image_data):
        """Stable on appspot, not local"""
        """Hm, unstable everywhere"""
        image = images.Image(image_data)
        result = urlfetch.Fetch(self.__watermark_addr) 
        watermark = images.Image(result.content)
        if watermark.width > image.width:
            watermark.resize(image.width)
            watermark.execute_transforms(images.JPEG)
        watermarked_image = images.composite(
                                                 [ 
                                                    (image_data, 0, 0, 1.0, images.TOP_LEFT),
                                                    (watermark._image_data, 0, 0, 0.5, images.BOTTOM_CENTER)
                                                 ], 
                                                    image.width, image.height, 0, images.JPEG)
        return watermarked_image

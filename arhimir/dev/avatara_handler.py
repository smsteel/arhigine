from google.appengine.ext import db
from google.appengine.api import images
from output_class import OutputClass

class AvataraHandler(OutputClass):
    
    url_handler = '/show_avatara/.*'
    
    def get(self):
        resize = self.request.get('resize').split("x") if self.request.get('resize') else False
        try:
            if resize:
                self.userid = int(self.request.uri.split('?')[0].split('/')[-1])
            else:
                self.userid = int(self.request.uri.split('/')[-1])
        except:
            return
        
        avataras = db.GqlQuery("SELECT * FROM DBAvatara where userid = :dbuserid", 
                               dbuserid = int(self.userid))
        for avatara in avataras:
            self.response.headers['Content-Type'] = 'image/jpeg'
            image = images.Image(avatara.image)
            if resize:
                image.resize(int(resize[0]), int(resize[1]))
                image.execute_transforms(images.JPEG)
            self.response.out.write(image._image_data)
            return
        self.redirect('/images/default_userpic.png')

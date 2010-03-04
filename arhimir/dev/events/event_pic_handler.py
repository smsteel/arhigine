from google.appengine.ext import db
from output_class import OutputClass

class EventPicHandler(OutputClass):
    
    url_handler = '/show_event_pic/.*'
    
    def get(self):
        try:
            self.eventid = int(self.request.uri.split('/')[-1])
        except:
            return        
        pics = db.GqlQuery("SELECT * FROM DBEventPicture where eventid = :dbeventid", 
                               dbeventid = int(self.eventid))
        for pic in pics:        
            self.response.headers['Content-Type'] = 'image/jpeg'
            self.response.out.write(pic.image)
            return
        self.redirect('/images/default_event.png')

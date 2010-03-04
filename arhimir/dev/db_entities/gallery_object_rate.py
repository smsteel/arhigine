from google.appengine.ext import db

class DBGalleryObjectRate(db.Model):
    voter = db.IntegerProperty()
    object = db.IntegerProperty()
    is_nice = db.BooleanProperty()
    date = db.DateTimeProperty(auto_now_add = True)
    
    def vote(self, userid, object_id, is_nice):
        try:
            self.voter = userid
            self.object = object_id
            self.is_nice = is_nice
            self.put()
            return True
        except: return False
        
    def still_can_vote(self, userid, object_id):
        entities = self.gql("where voter = :uid and object = :ok", uid = userid, ok = object_id)
        return (not bool(entities.count()))


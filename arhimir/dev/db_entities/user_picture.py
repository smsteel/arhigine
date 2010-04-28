from google.appengine.ext import db

class DBAvatara(db.Model):
    userid = db.IntegerProperty()
    image = db.BlobProperty()
    
    def get_by_userid(self, userid):
        try:
            db.GqlQuery("SELECT __key__ FROM DBAvatara WHERE userid = :userid", userid=userid)[0]
            return True
        except:
            return False

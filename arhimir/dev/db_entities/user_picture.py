from google.appengine.ext import db

class DBAvatara(db.Model):
    userid = db.IntegerProperty()
    image = db.BlobProperty()

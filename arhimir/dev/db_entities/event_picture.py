from google.appengine.ext import db

class DBEventPicture(db.Model):
    eventid = db.IntegerProperty()
    image = db.BlobProperty()

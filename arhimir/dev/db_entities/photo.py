from google.appengine.ext import db

class DBPhoto(db.Model):
    image_small = db.BlobProperty()
    image_big = db.BlobProperty()
    albumid = db.IntegerProperty()
    tags = db.TextProperty()
    comment = db.StringProperty()
    date = db.DateTimeProperty(auto_now_add = True)
    
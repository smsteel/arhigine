from google.appengine.ext import db

class Banner(db.Model):
    name = db.StringProperty()
    link = db.StringProperty()
    image = db.BlobProperty()
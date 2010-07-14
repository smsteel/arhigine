from google.appengine.ext import db

class DBPhotoTags(db.Model):
    tags = db.TextProperty()
    imageid = db.IntegerProperty()
    fixed = db.BooleanProperty(default = False)

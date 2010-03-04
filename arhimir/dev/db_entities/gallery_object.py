from google.appengine.ext import db

class DBGalleryObject(db.Model):
    userid = db.IntegerProperty()
    image = db.BlobProperty()
    name = db.StringProperty()
    smalldescription = db.TextProperty()
    description = db.TextProperty()
    date = db.DateTimeProperty(auto_now_add = True)


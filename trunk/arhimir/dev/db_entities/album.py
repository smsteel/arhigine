from google.appengine.ext import db

class DBAlbum(db.Model):
    objectid = db.IntegerProperty()
    name = db.StringProperty()
    userid = db.IntegerProperty()
    date = db.DateTimeProperty(auto_now_add = True)

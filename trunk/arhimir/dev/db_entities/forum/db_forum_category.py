from google.appengine.ext import db

class DBForumCategory(db.Model):
    name = db.StringProperty()
    access = db.IntegerProperty()
    position = db.IntegerProperty()

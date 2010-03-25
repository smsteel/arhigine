from google.appengine.ext import db

class DBForumCategory(db.Model):
    name = db.StringProperty()
    descr = db.TextProperty()
    access = db.IntegerProperty()
    position = db.IntegerProperty()

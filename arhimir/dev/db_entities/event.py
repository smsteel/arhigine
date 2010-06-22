from google.appengine.ext import db
from db_entities.user import DBUser

class DBEvent(db.Model):
    name = db.StringProperty()
    mini_descr = db.TextProperty()
    descr = db.TextProperty()
    date = db.DateProperty()
    time = db.StringProperty()
    place = db.StringProperty()
    owner = db.StringProperty()
    access = db.IntegerProperty()
    userid = db.IntegerProperty()
    catid = db.IntegerProperty()
    author = db.ReferenceProperty(DBUser)
    closed = db.BooleanProperty(default = False)
    
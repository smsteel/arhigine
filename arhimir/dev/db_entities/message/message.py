from google.appengine.ext import db
from db_entities.user import DBUser

class Message(db.Model):
    owner = db.ReferenceProperty(DBUser)
    title = db.StringProperty()
    body = db.TextProperty()
    read = db.BooleanProperty(default = False)
    deleted = db.BooleanProperty(default = False)
    datetime = db.DateTimeProperty(auto_now_add = True)
    
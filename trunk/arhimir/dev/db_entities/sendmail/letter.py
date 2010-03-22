from google.appengine.ext import db
from db_entities.user import DBUser

class Letter(db.Model):
    datetime = db.DateTimeProperty(auto_now_add = True)
    to = db.ReferenceProperty(DBUser)
    subject = db.StringProperty()
    body = db.TextProperty()
    
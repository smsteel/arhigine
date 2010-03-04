from google.appengine.ext import db
from db_entities.user import DBUser

class Letter(db.Model):
    to = db.ReferenceProperty(DBUser)
    subject = db.StringProperty()
    body = db.TextProperty()
    
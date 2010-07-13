from google.appengine.ext import db
from db_entities.user import DBUser

class TagsList(db.Model):
    entity = db.ReferenceProperty()
    tags = db.StringListProperty()
    user = db.ReferenceProperty(DBUser)
    datetime = db.DateTimeProperty(auto_now_add = True)
    
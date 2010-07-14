from google.appengine.ext import db
from db_entities.user import DBUser

class TagsList(db.Model):
    obj = db.ReferenceProperty(collection_name="taged_objects")
    tags = db.StringListProperty()
    user = db.ReferenceProperty(DBUser, collection_name="tager_user")
    datetime = db.DateTimeProperty(auto_now_add = True)
    
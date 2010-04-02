from google.appengine.ext import db
from db_entities.user import DBUser

class DBComments(db.Model):
    obj = db.ReferenceProperty(collection_name="objects")
    content = db.TextProperty()
    date = db.DateTimeProperty(auto_now_add = True)
    user = db.ReferenceProperty(DBUser, collection_name="users")
    parent_comment = db.SelfReferenceProperty(collection_name="parent_comments")
    rating = db.IntegerProperty()
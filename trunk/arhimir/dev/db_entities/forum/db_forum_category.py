from google.appengine.ext import db
from db_entities.comments import DBComments

class DBForumCategory(db.Model):
    name = db.StringProperty()
    descr = db.TextProperty()
    access = db.IntegerProperty()
    position = db.IntegerProperty()
    last_comment = db.ReferenceProperty(DBComments)
    comments_count = db.IntegerProperty(default = 0)
    topics_count = db.IntegerProperty(default = 0)

from google.appengine.ext import db
from db_entities.forum.db_forum_category import DBForumCategory
from db_entities.user import DBUser

class DBForumTopic(db.Model):
    date = db.DateTimeProperty(auto_now_add = True)
    name = db.StringProperty()
    description = db.TextProperty()
    category = db.ReferenceProperty(DBForumCategory)
    author = db.ReferenceProperty(DBUser)
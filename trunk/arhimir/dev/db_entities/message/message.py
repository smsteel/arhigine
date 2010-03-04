from google.appengine.ext import db
from db_entities.user import DBUser

class Message(db.Model):
    owner = db.ReferenceProperty(DBUser)
    title = db.StringProperty()
    body = db.TextProperty()
    show_to_owner = db.BooleanProperty(default=True)
    
    def has_unread_msg(self, userid):
        return 0
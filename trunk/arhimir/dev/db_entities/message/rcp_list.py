from google.appengine.ext import db
from db_entities.user import DBUser
from db_entities.message.message import Message

class Rcp_list(db.Model):
    message = db.ReferenceProperty(Message)
    rcp = db.ReferenceProperty(DBUser)
    read = db.BooleanProperty(default = False)
    deleted = db.BooleanProperty(default = False)
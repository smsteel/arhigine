#just add some water!
from google.appengine.ext import db

class DBInvite(db.Model):
    hash = db.StringProperty()
    userid = db.IntegerProperty()
    date = db.DateProperty(auto_now_add = True)
    used = db.BooleanProperty(default = False)
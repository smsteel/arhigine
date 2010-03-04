from google.appengine.ext import db

class DBSession(db.Model):
    sid = db.StringProperty()
    userid = db.IntegerProperty()
    authorized = db.BooleanProperty(default=False)
    login = db.StringProperty()

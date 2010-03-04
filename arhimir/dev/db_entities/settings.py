from google.appengine.ext import db

class DBSettings(db.Model):
    name = db.StringProperty()
    val = db.IntegerProperty()
    textval = db.TextProperty()

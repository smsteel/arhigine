from google.appengine.ext import db

class DBConf(db.Model):
    name = db.StringProperty()
    cap = db.StringProperty()
    rules = db.TextProperty()
    about = db.TextProperty()
    userid = db.IntegerProperty()
    updated = db.DateTimeProperty(auto_now_add = True)
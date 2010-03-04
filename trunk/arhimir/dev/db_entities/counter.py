from google.appengine.ext import db

class DBCounter(db.Model):
    eventid = db.IntegerProperty()
    userid = db.IntegerProperty()
    hit = db.IntegerProperty(default = 0)
    visit = db.IntegerProperty(default = 0)

from google.appengine.ext import db

class DBPage(db.Model):
    name = db.StringProperty()
    title = db.StringProperty()
    content = db.TextProperty()
    userid = db.IntegerProperty()
    date = db.DateTimeProperty(auto_now = True)
    
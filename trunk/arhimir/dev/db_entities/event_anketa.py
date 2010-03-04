from google.appengine.ext import db

class DBEventAnketa(db.Model):
    userid = db.IntegerProperty()
    eventid = db.IntegerProperty()
    name = db.StringProperty()
    surname = db.StringProperty()
    phone = db.StringProperty()
    email = db.StringProperty()
    company = db.StringProperty()
    position = db.StringProperty()
    payway = db.IntegerProperty()
    is_portfolio = db.BooleanProperty(default = False)
    additional = db.TextProperty()
    isarhitect = db.BooleanProperty()
    date = db.DateTimeProperty(auto_now_add = True)
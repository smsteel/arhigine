from google.appengine.ext import db

class DBDailyUsers(db.Model):
    date = db.DateProperty(auto_now_add = True)
    login = db.StringProperty()
    userid = db.IntegerProperty()

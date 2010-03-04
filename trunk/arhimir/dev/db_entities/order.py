from google.appengine.ext import db

class DBOrder(db.Model):
    arch = db.StringProperty()
    fio = db.StringProperty()
    phone = db.StringProperty()
    email = db.StringProperty()
    type = db.StringProperty()
    square = db.StringProperty()
    misc = db.TextProperty()
    status = db.StringProperty()
    date = db.DateProperty(auto_now_add = True)
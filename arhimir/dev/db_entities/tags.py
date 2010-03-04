from google.appengine.ext import db

class DBTags(db.Model):
    tags = db.TextProperty()
    date = db.DateProperty(auto_now_add = True)

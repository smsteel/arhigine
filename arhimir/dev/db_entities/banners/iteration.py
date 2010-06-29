from google.appengine.ext import db

class BannerIter(db.Model):
    number = db.IntegerProperty(default = 0)
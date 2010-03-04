# -*- coding: UTF-8 -*-

from google.appengine.ext import db

class DBTwit(db.Model):
    twit = db.TextProperty()
    user = db.StringProperty()


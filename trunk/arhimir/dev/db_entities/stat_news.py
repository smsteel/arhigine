from google.appengine.ext import db
from news import DBNews

class StatNews(db.Model):
    
    counter = db.IntegerProperty(default=0)
    pieceon = db.ReferenceProperty(DBNews)

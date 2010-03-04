from google.appengine.ext import db

class DBMSGRecipients(db.Model):
    recipient = db.IntegerProperty()
    message = db.ReferenceProperty()
    read = db.BooleanProperty(default=False)
    date = db.DateTimeProperty(auto_now_add=True)

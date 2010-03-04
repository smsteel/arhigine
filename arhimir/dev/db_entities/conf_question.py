from google.appengine.ext import db

class DBConfQuestion(db.Model):
    cap = db.StringProperty()
    text = db.TextProperty()
    userid = db.IntegerProperty()
    confid = db.IntegerProperty()
    answer = db.TextProperty()
    moderated = db.BooleanProperty(default = False)
    date = db.DateTimeProperty(auto_now_add = True)
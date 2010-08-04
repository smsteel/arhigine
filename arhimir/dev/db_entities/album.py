from google.appengine.ext import db
from comments import DBComments
from user import DBUser

class DBAlbum(db.Model):
    objectid = db.IntegerProperty()
    name = db.StringProperty()
    userid = db.IntegerProperty()
    author = db.ReferenceProperty(DBUser)
    date = db.DateTimeProperty(auto_now_add = True)
    last_comment = db.ReferenceProperty(DBComments)
    comments_count = db.IntegerProperty(default = 0)

    def increase_comments_count(self, comment):
        self.comments_count = self.comments_count + 1
        self.last_comment = comment
        self.put()
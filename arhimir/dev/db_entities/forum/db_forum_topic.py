from google.appengine.ext import db
from db_entities.forum.db_forum_category import DBForumCategory
from db_entities.user import DBUser
from db_entities.comments import DBComments

class DBForumTopic(db.Model):
    date = db.DateTimeProperty(auto_now_add = True)
    name = db.StringProperty()
    description = db.TextProperty()
    category = db.ReferenceProperty(DBForumCategory)
    author = db.ReferenceProperty(DBUser)
    last_comment = db.ReferenceProperty(DBComments)
    comments_count = db.IntegerProperty(default = 0)

    def increase_comments_count(self, comment):
        try:
            self.comments_count = self.comments_count + 1
        except:
            self.comments_count = 1
        try:   
            self.category.comments_count = self.category.comments_count + 1
        except: 
            self.category.comments_count = 1
        self.last_comment = comment
        
        self.category.last_comment = comment
        self.category.put()
        self.put()
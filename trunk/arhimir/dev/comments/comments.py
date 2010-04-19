from google.appengine.ext import db
from tools.tag_processor import tag_processor

class Comments():
    
    def getCommentsCount(self, entities):
        comments_count = 0
        for entity in entities:
            comments = db.GqlQuery("SELECT __key__ FROM DBComments WHERE obj = :entity", 
                                     entity = entity)
            comments_count += comments.count()
        return comments_count

    def getLastComment(self, entities):
        comments = db.GqlQuery("SELECT * FROM DBComments ORDER BY date DESC")
        if(comments.count()>0):
            for comment in comments:
                try:
                    if comment.obj.key() in entities:
                        return { 'date' : comment.date,
                                 'user' : { 'login': comment.user.login.encode("utf8") },
                                 'objid': comment.obj.key().id() }
                except: pass
            return False
        else:
            return False
    
    def getComments(self, obj):
            formalized_comments = []
            comments = db.GqlQuery("SELECT * FROM DBComments WHERE obj = :obj ORDER BY date", 
                                     obj = obj)
            for comment in comments:
                try:
                    if not comment.parent_comment and comment.content != "":
                        formalized_comments.append({ 
                                                     'login' : comment.user.login.encode("utf8"),
                                                     'content' : tag_processor().prepare(comment.content), 
                                                     'date' : comment.date,
                                                     'userid' : comment.user.key().id(),
                                                     'key' : comment.key(),
                                                  })
                        formalized_comments += self.getChildComments(comment)
                except: pass
            return formalized_comments

    def getChildComments(self, comment, level = 50):
        child_comments = []
        for child_comment in comment.parent_comments:
            child_comments.append({ 
                                    'login' : child_comment.user.login.encode("utf8"),
                                    'content' : tag_processor().prepare(child_comment.content),
                                    'date' : child_comment.date,
                                    'userid' : child_comment.user.key().id(),
                                    'key' : child_comment.key(),
                                    'level' : level,
                                 })
            
            child_comments += self.getChildComments(child_comment, level + 50)
            child_comment = None
        return sorted(child_comments, key=lambda k: k['date'])

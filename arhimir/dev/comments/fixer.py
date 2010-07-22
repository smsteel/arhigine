from google.appengine.ext import webapp
from comments import Comments

class Fixer(webapp.RequestHandler):
    
    url_handler = '/forum_fixer/?'
    
    def get(self):
        c = Comments()
        c.fixCommentsForTopics()
        c.fixCommentsForCategories()
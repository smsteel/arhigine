from output_class import OutputClass
from db_entities.comments import DBComments
from db_entities.user import DBUser
from google.appengine.ext import db
import cgi

class CommentHandler(OutputClass):
    
    url_handler = '/comments.*'
    access = 0
    def post(self):
        if super(CommentHandler, self).get():
            if not self.request.get("content"):
                self.showMessage("""Введите текст комментария!
                <br><a href='""" + self.request.headers.get("Referer") + """'>Вернуться в тему</a>""")
                return
            comment = DBComments()
            comment.user = DBUser.get_by_id(self.Session['userid'])
            
            comment.obj = db.Key(str(self.request.get('entity')))
            content = self.request.get("content")
            comment.content = cgi.escape(content).replace("\n", "<br />")
            comment.parent_comment = DBComments().get_by_id(int(self.request.get('parent_comment'))) if \
                                                            self.request.get('parent_comment') else None
            comment.put()
            self.redirect(self.request.headers.get("Referer"))
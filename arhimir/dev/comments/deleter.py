# -*- coding: UTF-8 -*-

from output_class import OutputClass
from db_entities.comments import DBComments
from google.appengine.ext import db

class CommentDeleter(OutputClass):
    
    url_handler = '/comment/delete/.*'
    
    def get(self):
        self.checkSession(self.request.headers.get('Cookie'))
        id = int(self.request.uri.split('/')[-1])
        comment = DBComments.get_by_id(id)
        #entityid = db.get(comment.obj.key()).key().id()
        if self.Session['access'] >= 8:
            db.delete(comment)
            self.showMessage("Комментарий удален!")
        else:
            self.showMessage("У вас недостаточно прав для выполнения данной операции")
        
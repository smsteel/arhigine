#coding: UTF-8

from output_class import OutputClass
from db_entities.comments import DBComments
from db_entities.user import DBUser
from google.appengine.ext import db
from google.appengine.ext.webapp import template
from sendmail.post_office import PostOffice
from db_entities.custom_field import DBCustomField
import cgi

class CommentHandler(OutputClass):
    
    url_handler = '/comments.*'
    access = 0
    
    def get(self):
        self.response.out.write(template.render("comments/comment_notification.html", {}))
    
    def post(self):
        if super(CommentHandler, self).get():
            if not self.request.get("content"):
                self.showMessage("""Введите текст комментария!
                <br><a href='""" + self.request.headers.get("Referer") + """'>Вернуться в тему</a>""")
                return
            comment = DBComments()
            user = DBUser.get_by_id(self.Session['userid'])
            comment.user = user
            if user.comments_count:
                user.comments_count = user.comments_count + 1
            user.put()
            
            comment.obj = db.Key(str(self.request.get('entity')))
            content = self.request.get("content")
            comment.content = cgi.escape(content).replace("\n", "<br />")
            
            comment.parent_comment = DBComments().get(self.request.get('parent_comment')) if \
                                     self.request.get('parent_comment') else None
            # Old part with id
            #DBComments().get_by_id(int(self.request.get('parent_comment'))) if \
            #                       self.request.get('parent_comment') else None
            
            key_ = comment.put()
            comment = db.get(key_)

            try:
                comment.obj.increase_comments_count(comment)
            except: pass


            #Отсылаем владельцу топика
            if self.Session['user_key'] != comment.obj.author.key():
                body = template.render("comments/comment_notification.html", { 
                                                                                'user' : self.Session,
                                                                                'comment' : comment,
                                                                                'referer' : self.request.headers.get("Referer"),
                                                                                'site_url' : DBCustomField().getByName('url')
                                                                              })
                PostOffice().append_to_queue(comment.obj.author.key(), """Новый комментарий на портале Архимир""".decode("utf-8"), body.decode("utf-8"))
                
            #Отсылаем владельцу коммента-предка:
            if comment.parent_comment and \
            (self.Session['user_key'] != comment.parent_comment.user.key()) and \
            (comment.obj.author.key() != comment.parent_comment.user.key()):
                body = template.render("comments/comment_notification.html", { 
                                                                                'to_parent' : True,
                                                                                'user' : self.Session,
                                                                                'comment' : comment,
                                                                                'referer' : self.request.headers.get("Referer"),
                                                                                'site_url' : DBCustomField().getByName('url')
                                                                              })
                PostOffice().append_to_queue(comment.parent_comment.user.key(), """Новый комментарий на портале Архимир""".decode("utf-8"), body.decode("utf-8"))
            self.redirect(self.request.headers.get("Referer"))
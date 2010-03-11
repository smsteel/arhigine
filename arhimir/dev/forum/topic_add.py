# -*- coding: UTF-8 -*-

from db_entities.forum.db_forum_topic import DBForumTopic
from db_entities.forum.db_forum_category import DBForumCategory
from db_entities.comments import DBComments 
from db_entities.user import DBUser
from output_class import OutputClass
import cgi

class forum_topic_add(OutputClass):
    
    url_handler = '/forum/topic/add/.*'
    access = 0
    
    def get(self):
        """ Drawing topic adding form"""
        if super(forum_topic_add, self).get(): self.insertMenu()
        else: return
        self.insertTemplate("forum/topic_add.html", {})
        self.drawPage("Добавление категории в форум")

    def post(self):
        if not super(forum_topic_add, self).get(): return
        cat_id = int(self.get_url_part(1))
        new_topic = DBForumTopic()
        new_topic.name = cgi.escape(self.request.get("name"))
        new_topic.description = cgi.escape(self.request.get("descr")).replace("\n", "<br />")
        new_topic.category = DBForumCategory.get_by_id(cat_id).key()
        new_topic.author = DBUser.get_by_id(self.Session['userid']).key()
        
        info_comment = DBComments() #one of them
        info_comment.user = new_topic.author
        info_comment.obj = new_topic.put()
        info_comment.content = ""
        info_comment.put()
        
        self.showMessage("Добавлено")
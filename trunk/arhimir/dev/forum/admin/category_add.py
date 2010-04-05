#coding: UTF-8

from db_entities.forum.db_forum_category import DBForumCategory
from output_class import OutputClass
import cgi

class forum_category_add(OutputClass):
    
    url_handler = '/forum/admin/category/add/?'
    access = 10
    
    def get(self):
        if not super(forum_category_add, self).get(): return
        self.insertTemplate('forum/category_anketa.html', {})
        self.drawPage("Добавление категории в форум")

    def post(self):
        if not super(forum_category_add, self).get(): return
        new_category = DBForumCategory()
        new_category.name = cgi.escape(self.request.get("name"))
        new_category.descr = cgi.escape(self.request.get("descr"))
        new_category.access = 0
        new_category.position = 0
        new_category.put()
        self.showMessage("Добавлено")
# -*- coding: UTF-8 -*-

from output_class import OutputClass
from db_entities.forum.db_forum_category import DBForumCategory
import cgi

class forum_category_edit(OutputClass):
    
    url_handler = '/forum/admin/category/edit/.+'
    access = 10

    def get(self):
        if not super(forum_category_edit, self).get(): return
        category = None
        cat = int(self.get_url_part(1))

        try:
            category = DBForumCategory.get_by_id(cat)
        except:
            self.showMessage("Категория не найдена!")
            return 
        
        self.insertTemplate('forum/category_anketa.html', {'cat':category})
        self.drawPage("Редактирование категории")
        
    def post(self):
        if not super(forum_category_edit, self).get(): return
        cat = int(self.get_url_part(1))
        category = DBForumCategory.get_by_id(cat)
        category.name = cgi.escape(self.request.get("name"))
        category.descr = cgi.escape(self.request.get("descr"))
        category.put()
        self.showMessage("Добавлено")
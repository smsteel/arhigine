# -*- coding: UTF-8 -*-

from output_class import OutputClass
from google.appengine.ext import db
from comments.comments import Comments
from db_entities.forum.db_forum_category import DBForumCategory
from tools.multipage import Multipage

class forum_category(OutputClass):
    
    url_handler = '/forum/category/?'

    def get(self):
        self.checkSession(self.request.headers.get('Cookie'), False)
        category = 0
        cat = int(self.request.get('cat')) if self.request.get('cat') else 0#int(self.get_url_part(1))

        cat_name = "Not set"

        try:
            category = DBForumCategory.get_by_id(cat)
            cat_name = category.name.encode("utf-8")
        except:
            self.showMessage("Категория не найдена!")
            return 
        
        _topics = []
        comments = Comments()
        #page = self.request.get(')
        
        try:
            tops = db.GqlQuery("SELECT * FROM DBForumTopic where category = :category", category = category.key()) 
            for top in tops:
                last_message = comments.getLastComment([top.key()])
                _topics.append({'id':int(top.key().id()), 'name':top.name.encode("utf-8"), 
                                'answers' : comments.getCommentsCount([top.key()]) - 1,
                                'last_message' : last_message })
        except: pass
        _topics.reverse()
        multipage = Multipage(self.request.get('page'), _topics, '/forum/category&cat=' + str(cat))
        self.insertTemplate('forum/category.html', {
                                                    'tops': multipage.getItems(),
                                                    'pages': multipage.getPages(),
                                                    'cat_name':cat_name,
                                                    'cat_id':cat 
                                                    })
        self.drawPage("Форум :: Просмотр категории "+cat_name)
        
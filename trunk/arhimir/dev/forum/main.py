#coding: UTF-8

from output_class import OutputClass
from google.appengine.ext import db
#from comments.comments import Comments
#from db_entities.forum.db_forum_topic import DBForumTopic
from db_entities.user import DBUser

class forum_main(OutputClass):
    
    url_handler = '/forum/?'
    
    def get(self):
        
        self.checkSession(self.request.headers.get('Cookie'), False)
        
        is_admin = False
        if self.Session['access'] == 10: is_admin = True
        
        _categories = []
        
        cats = db.GqlQuery("SELECT * FROM DBForumCategory order by position") 
        #comments = Comments()

        all_comments_count = 0
        all_topics_count = 0
        for cat in cats:
            
            #topics = db.GqlQuery("SELECT * FROM DBForumTopic where category = :cat", cat = cat.key())
            if cat.access and not cat.access <= self.Session['access']: continue
            try:
                all_comments_count += cat.comments_count
                all_topics_count += cat.topics_count
            except:
                pass

            try:
                cat.last_comment.obj.name = cat.last_comment.obj.name[0:32] + "..." if len(cat.last_comment.obj.name) > 32 else cat.last_comment.obj.name
            except:
                pass
            _categories.append({'id':int(cat.key().id()), 'name':cat.name.encode("utf-8"),
                                'descr': cat.descr.encode("utf-8") if cat.descr else None,
                                'last_message' : cat.last_comment,
                                'answers' : cat.comments_count,
                                'topics' : cat.topics_count
                                #'last_message' : last_message, 'answers' : comments_count, 'topics' : len(formilized_topics)
                                })
            
        self.insertTemplate('forum/forum_main.html', {
                                                      'cats':_categories,
                                                      'is_admin': is_admin,
                                                      'all_comments_count' : all_comments_count,
                                                      'all_topics_count' : all_topics_count,
                                                      'logged' : self.Session['authorized'],
                                                      'your_comments' : DBUser().count_comments(self.Session['user_key'])
                                                     })
        self.drawPage("Форум")
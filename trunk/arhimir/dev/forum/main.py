# -*- coding: UTF-8 -*-

from output_class import OutputClass
from google.appengine.ext import db
from comments.comments import Comments
from db_entities.forum.db_forum_topic import DBForumTopic

class forum_main(OutputClass):
    
    url_handler = '/forum/?'
    
    def get(self):
        
        self.checkSession(self.request.headers.get('Cookie'), False)
        
        _categories = []
        
        cats = db.GqlQuery("SELECT * FROM DBForumCategory order by position") 
        comments = Comments()
        for cat in cats:
            topics = db.GqlQuery("SELECT * FROM DBForumTopic where category = :cat", cat = cat.key())
            formilized_topics = []
            for topic in topics:
                formilized_topics.append(topic.key())
            last_message = comments.getLastComment(formilized_topics)
            if last_message:
                topic = DBForumTopic.get_by_id(last_message['objid'])
                topic_name = topic.name
                last_message['topic'] = { 'name' : topic_name[0:32] + "..." if len(topic_name) > 32 else topic_name,
                                          'id' : int(topic.key().id()) }
            _categories.append({'id':int(cat.key().id()), 'name':cat.name.encode("utf-8"),
                                'last_message' : last_message, 'descr': cat.descr.encode("utf-8"),
                                'answers' : comments.getCommentsCount(formilized_topics) })
        
        self.insertTemplate('forum/forum_main.html', {'cats':_categories})
        self.drawPage("Форум")
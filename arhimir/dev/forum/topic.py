# -*- coding: UTF-8 -*-

from output_class import OutputClass
from db_entities.forum.db_forum_topic import DBForumTopic
from tools.tag_processor import tag_processor

class forum_topic(OutputClass):
    
    url_handler = '/forum/topic/.*'
    access = -1
    
    def get(self):
        super(forum_topic, self).get(redirect=False)
        topic_id = int(self.get_url_part(1))
        
        topic = None
        
        try:
            topic = DBForumTopic.get_by_id(topic_id)
        except:
            self.showMessage("Тема не найдена!")
            return 
        
        t_p = tag_processor()
        topic_text = t_p.prepare(topic.description.encode("utf-8"))
        
        self.insertTemplate('forum/topic.html', {'user_name':topic.author.login ,'top_name':topic.name.encode("utf-8"), 'top_descr':topic_text})
        self.insertComments(topic.key())
        self.drawPage("Форум :: Просмотр темы "+topic.name.encode("utf-8"))

# -*- coding: UTF-8 -*-

from db_entities.forum.db_forum_topic import DBForumTopic
from output_class import OutputClass
import cgi

class forum_topic_edit(OutputClass):
    
    url_handler = '/forum/topic/edit/.*'
    access = 8
    
    def get(self):
        """ Drawing topic adding form"""
        topic_id = int(self.get_url_part(1))
        
        topic = None
        
        try:
            topic = DBForumTopic.get_by_id(topic_id)
        except:
            self.showMessage("Тема не найдена!")
            return 
        
        if super(forum_topic_edit, self).get(topic.author.key().id()): self.insertMenu()
        else: return
        
        formalized_topic = {}
        
        formalized_topic['description'] = topic.description.replace('<br />', '\n')
        formalized_topic['name'] = topic.name
        
        self.insertTemplate("forum/topic_add.html", {'topic':formalized_topic})
        self.drawPage("Редактирование топика")

    def post(self):
        
        topic_id = int(self.get_url_part(1))
        
        topic = DBForumTopic.get_by_id(topic_id)

        if super(forum_topic_edit, self).get(topic.author.key().id()): self.insertMenu()
        else: return
        
        topic.name = cgi.escape(self.request.get("name"))
        topic.description = cgi.escape(self.request.get("descr")).replace("\n", "<br />")
        
        topic.put()
        
        self.showMessage("Изменено")
        
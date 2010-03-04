# -*- coding: UTF-8 -*-

from output_class import OutputClass
from db_entities.conf import DBConf
from db_entities.conf_question import DBConfQuestion
import cgi

class ConfAsk(OutputClass):
    
    url_handler = '/conf/ask/.*'
    access = 0
    
    def get(self):

        super(ConfAsk, self).get()

        name = self.get_url_part(1)
        
        conf = 0
        
        try:
            conf = DBConf.gql("where name = :name", name = name)[0]
        except:
            self.showMessage("К сожалению, такой конференции не найдено!")
            return

        self.insertTemplate("conf/tpl_conf_ask.html", {
                                              'name' : name,
                                              'cap' : conf.cap,
                                              })
        self.drawPage("Конференция :: "+str(conf.name))
        
    def post(self):
    
        super(ConfAsk, self).get()
    
        name = self.get_url_part(1)
        
        conf = 0
        
        try:
            conf = DBConf.gql("where name = :name", name = name)[0]
        except:
            self.showMessage("К сожалению, такой конференции не найдено!")
            return
        
        question = DBConfQuestion()
        question.cap = cgi.escape(self.request.get("cap"))
        question.text = cgi.escape(self.request.get("text"))
        question.confid = conf.key().id()
        question.userid = self.Session['userid']
        
        question.put()
        
        self.showMessage("Спасибо за Ваш вопрос!")
        
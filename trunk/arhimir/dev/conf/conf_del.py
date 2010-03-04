# -*- coding: UTF-8 -*-

from output_class import OutputClass
from db_entities.conf import DBConf
from db_entities.conf_question import DBConfQuestion
from google.appengine.ext import db

class ConfDel(OutputClass):
    
    url_handler = '/conf/delete/.*'
    access = 0
    
    def get(self):

        super(ConfDel, self).get()

        q_id = int(self.get_url_part(1))
        name = self.get_url_part(2)
        
        conf = 0
     
        try:
            conf = DBConf.gql("where name = :name", name = name)[0]
        except:
            self.showMessage("К сожалению, такой конференции не найдено!")
            return

        if conf.userid != self.Session['userid']:
            self.showMessage("Нет доступа")
            return
        
        question = DBConfQuestion.get_by_id(q_id)
        db.delete(question)
        
        self.showMessage("Удалено!")
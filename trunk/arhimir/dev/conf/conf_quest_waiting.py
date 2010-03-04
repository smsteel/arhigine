# -*- coding: UTF-8 -*-

from output_class import OutputClass
from db_entities.conf import DBConf
from db_entities.conf_question import DBConfQuestion
from db_entities.user import DBUser

class ConfQuestWaiting(OutputClass):
    
    url_handler = '/conf/waiting/.*'
    access = 0
    
    def get(self):

        super(ConfQuestWaiting, self).get()

        name = self.get_url_part(1)
        
        conf = 0
        
        try:
            conf = DBConf.gql("where name = :name", name = name)[0]
        except:
            self.showMessage("К сожалению, такой конференции не найдено!")
            return

        if conf.userid != self.Session['userid']:
            self.showMessage("Нет доступа")
            return
        
        #_questions = DBConfQuestion.all().filter("confid =", conf.key().id()).filter("moderated = ", False)
        _questions = DBConfQuestion.gql("where confid = :cid and moderated = :m", cid = conf.key().id(), m = False)
        questions = []
        for q in _questions:
            user = DBUser()
            questions.append(
                             {
                              'id' : q.key().id(),
                              'cap' : q.cap,
                              'text' : q.text,
                              'user' : user.get_login_by_id(q.userid),
                              'date' : q.date,
                             }
                             )
        questions.reverse()        
        self.insertTemplate("conf/tpl_conf_waiting.html", {
                                              'name' : name,
                                              'cap' : conf.cap,
                                              'questions' : questions,
                                              })

        self.drawPage("Конференция :: "+str(conf.name))
        
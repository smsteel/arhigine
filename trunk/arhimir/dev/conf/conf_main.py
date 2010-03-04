# -*- coding: UTF-8 -*-

from output_class import OutputClass
from db_entities.conf import DBConf
from google.appengine.ext import db
from db_entities.user import DBUser

class ConfMain(OutputClass):

    url_handler = '/conf/.*'

    def get(self):
        
        self.checkSession(self.request.headers.get('Cookie'), False)

        name = self.get_url_part(1)
        
        conf = 0

#        conf = DBConf()
#        conf.name = "arhimir"
#        conf.cap = "title"
#        conf.rules = "rules"
#        conf.about = "about"
#        conf.userid = 2
#        conf.put()
        
        try:
            conf = DBConf.gql("where name = :name", name = name)[0]
        except:
            self.showMessage("К сожалению, такой конференции не найдено!")
            return

        owner = False
        if int(conf.userid) == self.Session['userid']:
            owner = True
        _questions = db.GqlQuery("SELECT * FROM DBConfQuestion WHERE moderated=True") 
        
        
        #DBConfQuestion.gql("where answer != :some", some = None)#.filter("confid = ", conf.key().id())
        questions = []
        for q in _questions:
            user = DBUser()
            questions.append(
                             {
                              'id' : q.key().id(),
                              'cap' : q.cap,
                              'text' : q.text,
                              'user' : user.get_login_by_id(q.userid),
                              'answer' : q.answer,
                              'date' : q.date,
                             }
                             )
        questions.reverse()   
        self.insertTemplate("conf/tpl_conf.html", {
                                              'name' : name,
                                              'cap' : conf.cap,
                                              'questions' : questions,
                                              'owner' : owner,
                                              })
        self.drawPage("Конференция :: "+str(conf.name))
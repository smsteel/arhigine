# -*- coding: UTF-8 -*-

from output_class import OutputClass
from db_entities.conf import DBConf

class ConfRules(OutputClass):

    url_handler = '/conf/rules/.*'

    def get(self):

        name = self.get_url_part(1)
        
        conf = 0
     
        try:
            conf = DBConf.gql("where name = :name", name = name)[0]
        except:
            self.showMessage("К сожалению, такой конференции не найдено!")
            return
       
        self.insertTemplate("conf/tpl_conf_rules.html", {
                                              'name' : name,
                                              'cap' : conf.cap,
                                              'rules': conf.rules,
                                              })
        
        self.drawPage()
        
        
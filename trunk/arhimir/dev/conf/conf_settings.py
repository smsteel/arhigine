# -*- coding: UTF-8 -*-

from output_class import OutputClass
from db_entities.conf import DBConf

class ConfSettings(OutputClass):
    
    url_handler = '/conf/settings/.*'
    access = 0
    
    def get(self):

        super(ConfSettings, self).get()

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
        
        self.insertTemplate("conf/tpl_conf_settings.html", {
                                              'name' : name,
                                              'cap' : conf.cap,
                                              'about': conf.about,
                                              'rules': conf.rules,
                                              })
        
        self.drawPage()
        
    def post(self):
        
        super(ConfSettings, self).get()

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
        
        conf.about = self.request.get("about")
        conf.rules = self.request.get("rules")
        conf.put()
        
        self.showMessage("Готово!")
        
        
        
        
        
        
        
        
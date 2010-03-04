# -*- coding: UTF-8 -*-﻿﻿
#from google.appengine.ext import db
from output_class import OutputClass
from db_entities.event_categories import DBEventCat


class EventCategories(OutputClass):

    url_handler = '/admin/event/categories/?'
    access = 10

    def get(self):
        if not super(EventCategories, self).get(): return
        
        ec = DBEventCat()
        cats = ec.get_categories()
        
        self.insertTemplate("tpl_event_categories.html", {
                                                          'cats' : cats,
                                                          })
        
        self.drawPage('Управление категориями')
    

# -*- coding: UTF-8 -*-﻿﻿
#from google.appengine.ext import db
from output_class import OutputClass
from db_entities.event_categories import DBEventCat


class EventCategoriesAdd(OutputClass):

    url_handler = '/admin/event/categories/add/?'
    access = 10

    def get(self):
        if not super(EventCategoriesAdd, self).get(): return
        self.insertMenu()
        self.insertTemplate("tpl_event_categories_add.html", {
                                                     
                                                          })
        
        self.drawPage('Управление категориями')
    
    def post(self):
        if not super(EventCategoriesAdd, self).get(): return
        self.insertMenu()
        
        cat = DBEventCat()
        
        cat.name = self.request.get('name')
        cat.descr = self.request.get('descr')
        cat.put()
        
        self.showMessage("Категория добавлена")
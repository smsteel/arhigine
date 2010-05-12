# -*- coding: UTF-8 -*-
from google.appengine.api import memcache
from output_class import OutputClass

class CashReset(OutputClass):
    
    access = 10
    url_handler = '/reset/?'
    
    def get(self):
        memcache.flush_all()
        self.showMessage('Кеш очищен')



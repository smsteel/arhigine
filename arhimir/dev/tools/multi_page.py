# -*- coding: UTF-8 -*-

""" Горынычу посвящается """

from google.appengine.api import memcache
from output_class import OutputClass
import pickle

class MultiPage(OutputClass):
    
   
    def _getPages(self, type):
        data = memcache.get("pages_" + str(type))
        if not data:
            self.showMessage("Произошла неведомая ошибка.")
            return
        return pickle.loads(data)

    def get(self):
        if self.request.get("load"):
            id = int(self.request.get("load"))
            object = self._getSortedObjects()[id]
            self.response.out.write(str(object[0]))

    def render(self):
        pass
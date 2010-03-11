# -*- coding: UTF-8 -*-
from output_class import OutputClass

class Menu(OutputClass):
    
    access = 0
    url_handler = '/message/?'
    
    def get(self):
        if super(Menu, self).get(): self.insertMenu()
        else: return
        self.insertTemplate("message/menu.html")
        self.drawPage("Личные сообщения")
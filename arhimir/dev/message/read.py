# -*- coding: UTF-8 -*-
from output_class import OutputClass
from message.handler import Handler

class Read(OutputClass):
    
    access = 0
    url_handler = '/message/read/.+'
    
    def get(self):
        if super(Read, self).get(): self.insertMenu()
        else: return
        
        user = str(self.Session['user_key'])
        message = self.get_url_part(1)
        
        letter = Handler().get_letter(message, user)
        
        self.insertTemplate("message/read.html", { 'message' : letter, 'user' : user})
        self.drawPage("Чтение сообщения")
        
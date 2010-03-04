# -*- coding: UTF-8 -*-﻿﻿
from output_class import OutputClass
from message.handler import Handler
from db_entities.user import DBUser

class Send(OutputClass):
    
    url_handler = '/msg/send/?'
    access = 0
    
    def get(self):
        if not super(Send, self).get(): return
        self.insertTemplate('message/send.html')
        self.drawPage()

    def post(self):
        if not super(Send, self).get(): return
        Handler().send(self.Session['user_key'], [DBUser().get_key_by_login(self.request.get('rcp_login'))], self.request.get('title'), self.request.get('body'))
        self.response.out.write("Отправлено.")

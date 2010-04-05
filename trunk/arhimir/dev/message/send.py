#coding: UTF-8
from output_class import OutputClass
from message.handler import Handler
from db_entities.user import DBUser

class Send(OutputClass):
    
    url_handler = '/message/send/.+'
    access = 0
    
    def get(self):
        if super(Send, self).get(): self.insertMenu()
        else: return
        username = self.get_url_part(1)
        self.insertTemplate('message/send.html', {'username': username})
        self.drawPage()

    def post(self):
        if not super(Send, self).get(): return
        username = self.get_url_part(1)
        Handler().send(self.Session['user_key'], [DBUser().get_key_by_login(username)], self.request.get('title'), self.request.get('body'))
        self.showMessage("Отправлено.")
#
#    def url(self):
#        return "/message/send/"
    
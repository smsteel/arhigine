# coding: UTF-8

from output_class import OutputClass
from mass_send.mass_sender import MassSender

class Interface(OutputClass):
    
    url_handler = '/admin/send/?'
    access = 10
    
    def get(self):
        if not super(Interface, self).get(): return
        self.insertTemplate("mass_sender/send_form.html", {'body': self.insertFckEdit('body')})
        self.drawPage("Массовая рассылка")
    
    def post(self):
        if not super(Interface, self).get(): return
        type = self.request.get('type')
        subject = self.request.get('subject')
        body = self.request.get('body')
        
        if type == 1:
            MassSender().send_all(self, subject, body)
        elif type == 2:
            MassSender().send_arch(subject, body)
        else:
            MassSender().send_admin(subject, body)
        self.showMessage("Отправлено")
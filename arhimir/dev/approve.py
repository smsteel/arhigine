# -*- coding: UTF-8 -*-
from output_class import OutputClass
from sendmail.post_office import PostOffice
from db_entities.user import DBUser

class Approve(OutputClass):

    url_handler = '/user/approve/?'

    def get(self):
        self.checkSession(self.request.headers.get('Cookie'))
        self.insertMenu()
        if self.Session['access'] < 5: 
            self.insertTemplate("tpl_approve.html", { 'surname' : self.Session['surname'],
                                                      'name' : self.Session['name'] })
        else:
            self.insertContent("""Вы знаете, возможно это будет очень неожиданно, но вы уже архитектор.""")
        self.drawPage()

    def post(self):
        self.checkSession(self.request.headers.get('Cookie'))
        if self.Session['access'] < 5:
#            msgsend = MSGSender()
            content = (self.request.get('fio') + 
                "<br>" +
                self.request.get('phone') +
                "<br>" + self.request.get('position')+
                "<br>" +
                self.request.get('graduate') +
                "<br>" +
                self.request.get('exp')
            )
            caption = "Architector approve"
            try:
                PostOffice().append_to_queue(DBUser().get_key_by_login("spe"), caption, content)
                #msgsend.send_msg(self.Session['userid'], "smsteel", content, caption)
#                msgsend.send_msg(self.Session['userid'], "spe", content, caption)
                self.redirect("/msgbox/approvesend")
            except:
                self.redirect("/msgbox/approvefail")

#Хренотень для отправки мыла всем одминчегам            
#            users = DBUser.gql("where access = 10")
#            for user in users:
#                mail.send_mail(sender="no.reply.arhimir@gmail.com",
#                          to=str(user.email),
#                          subject="Запрос на повышение статуса до архитектора",
#                          body="""Пользователь """ + 
#                          self.Session['login'] + """
#подал заявку на повышение статуса. """)

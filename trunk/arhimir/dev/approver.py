#coding: UTF-8
from output_class import OutputClass
#from msg.msg_sender import MSGSender
import cgi
from db_entities.user import DBUser
from message.handler import Handler

class Approver(OutputClass):

    url_handler = '/approver/.*'
    access = 10
    
    def get(self):
        if not super(Approver, self).get(): return
        
        content = str(self.paramByName("new_arch"))
        caption = "Заявка на повышение урованя доступа"
        
        self.insertContent("""
        Это невообразимо адская форма. Убиться можно
        <br>
        <form method="post">
        <input type="hidden" name="caption" value='""" + caption + """'>
        <input type="hidden" name="content" value='""" + content + """'>
        <input type="submit" value="Да-да, я трезвый и в сознании">
        </form>
        """)
        self.drawPage("ppc")
    
    def post(self):
        if not super(Approver, self).get(): return
                          
        uri = self.request.uri
        uri = uri.split('/')
        login = str(cgi.escape(uri[-1]).split('?')[0]).replace("%40", "@")
                         
        try: 
            users = DBUser.gql("where login='%s'" % login)
            user = users[0]
            user.access = 6
            user.put()
        except:
            self.insertContent("Похоже логин некорректный")
        
#        caption = self.request.get("cap").encode("utf8")
#        content = self.request.get("content").encode("utf8")
        
#        self.insertContent(content)
        try:
            Handler().send(self.Session['user_key'], [DBUser().get_key_by_login(login)], self.request.get('caption'), self.request.get('content'))
#            msgsend = MSGSender()
#            msgsend.send_msg(-1, login, , )
            #PostOffice().append_to_queue(, self.request.get('caption'), self.request.get('content'))
        except:
            self.insertContent("Уведомлние не отправилось")
            
            
                          
        self.insertContent("""Готово""")
        self.drawPage()


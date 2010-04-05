#coding: UTF-8
from output_class import OutputClass
import cgi
from db_entities.user import DBUser
from sendmail.post_office import PostOffice

class MSGSend(OutputClass):
    
    #url_handler = '/msg/send/.+'
    
    def get(self):
        """ Show all msg captions """
        self.checkSession(self.request.headers.get('Cookie'))
        self.insertMenu()
        
        uri = self.request.uri
        uri = uri.split('/')
        recipient = str(cgi.escape(uri[-1]).split('?')[0]).replace("%40", "@")
        
        if recipient == str(self.Session['login']):
            self.insertContent("Нелья отправлять сообщение самому себе!")
            self.drawPage("Отправка сообщения")
            return
        
        self.insertContent("Сообщение для %s" % recipient)
        theme = self.request.GET['theme'].encode("utf8") if 'theme' in self.request.GET else '' 
        self.insertTemplate('tpl_msg_send.html', {'editor': self.insertFckEdit('content'), 'theme' : theme })
        self.drawPage("Отправка сообщения")

    def post(self):
        """ Write bullshit to DB"""        
        self.checkSession(self.request.headers.get('Cookie'))
        uri = self.request.uri
        uri = uri.split('/')
        recipient = str(cgi.escape(uri[-1]).split('?')[0]).replace("%40", "@")

        if recipient == str(self.Session['login']):
            self.insertContent("Нельзя отправлять сообщение самому себе!")
            self.drawPage("Отправка сообщения")
            return
        try:
            PostOffice().append_to_queue(DBUser().gql("WHERE login = :login", login = recipient)[0], self.request.get('caption'), self.request.get('content'))
            self.redirect('/msgbox/msgtrue')
        except:
            self.redirect('/msgbox/msgfalse')



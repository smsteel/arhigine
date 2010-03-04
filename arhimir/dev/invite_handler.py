from google.appengine.ext import db
from google.appengine.api import mail
import hashlib
from output_class import OutputClass
from db_entities.invite import DBInvite
import random

class InviteHandler(OutputClass):
    
    url_handler = '/invite/?'
    access = 8
    
    def get(self):
        if super(InviteHandler, self).get():
            self.checkSession(self.request.headers.get('Cookie'))
            self.insertMenu()
            if self.Session['access'] < 8:
                try:
                    
                    invites = db.GqlQuery("SELECT * FROM DBInvite where userid = :uid order by date desc",
                                           uid = int(self.Session['userid']) )
                    for invite in invites:
                        if db.datetime.date.today() == invite.date:
                            self.insertContent('Вы сегодня уже отправляли приглашение!')
                            self.drawPage()
                            return
                    
                except: pass
            self.insertContent("""
                <br>
                <table width=90% align=center>
                <tr>
                <td>
                <pre>
                Уважаемые пользователи, 
                теперь у Вас есть возможность воспользоваться новой функцией личного кабинета – «Приглашение».
                С помощью этой функции Вы сможете привлекать своих коллег и друзей архитекторов, дизайнеров на портал.
                Преимущество заключается в том, что они автоматически получат статус архитектора на портале,
                и смогут самостоятельно разместить свое портфолио и пользоваться другими функциями личного кабинета. 
                Однако, когда Вы отправляете приглашение новому участнику, Вы подтверждаете, что приглашаемый 
                является архитектором  или дизайнером. 
                Примите во внимание, что за нарушение этого правила к Вам могут быть применены соответствующие санкции.
                </pre>
                </td>
                </tr>
                <tr>
                <td>
                <form method="post">
                E-mail: <input type="text" name="email">
                <br>
                <input type="submit" value="Пригласить">
                
                </form>
                </td></tr></table>
            """)
            self.drawPage("Приглашения")
        
    def post(self):
        if super(InviteHandler, self).get():
            self.checkSession(self.request.headers.get('Cookie'))
            self.insertMenu()
            hash = str(hashlib.md5(str(self.Session['userid']+random.random())).hexdigest())
            this_invite = DBInvite()
            this_invite.hash = hash
            this_invite.userid = self.Session['userid']
            this_invite.put()
            
            email = str(self.request.get('email'))
            
            #self.insertContent(email)
            
            url = str("http://personal.arhimir.ru/reg/%s" % hash)
            #self.insertContent(url)
            
            try:
                mail.send_mail(sender="no.reply.arhimir@gmail.com",
                      to=str(email),
                      subject="Приглашение в Архимир!",
                      body="""Вас пригласили в Архимир! Вот Ваша уникальная ссылка для регистрации: """ + 
                      str(url) + """
        __
        С уважением, администрация arhimir.ru""")
                self.insertContent("Приглашение отправлено!")
            except:
                self.insertContent(""" Вы знаете... Жизнь сложная штука. И далеко не все в ней происходит так, как бы нам хотелось
                В жизни есть много мелочей, которые портят нам жизнь: отключили воду, пробки на дорогах и многое прочее. На этот раз произошел отказ всех систем.
                Поэтому приглашение не отправлено. Жаль. Правда. Можете связаться с кем-то из администрации. """)
            
            
            self.drawPage()
            
# -*- coding: UTF-8 -*-
from google.appengine.ext import db
import hashlib, cgi, random
from db_entities.user import DBUser
from db_entities.invite import DBInvite
from output_class import OutputClass
from register_confirm import RegisterConfirm
from sendmail.post_office import PostOffice

class RegisterHandler(OutputClass):
    """ Обработчик регистрации пользователей """
    
    url_handler = '/reg/.*|/checklog/.*|/checkmail/.*'
    
    def checkLogin(self, login):
        restricted = "~`!@#$%^&*()-=+\\/'\"{}][;:<>, "
        self.answer = ""
        for i in range(len(restricted)):
            if str(login).find(str(restricted[i])) >= 0:
                return False
    
        dbusers = db.GqlQuery("SELECT * FROM DBUser WHERE login = :login",
                              login = cgi.escape(login).lower())
        if len(str(login)) > 3:
            if int(dbusers.count()) == 0:
                self.answer = "Логин " + str(cgi.escape(login)) + " <font color = green>свободен</font>"
            else:
                self.answer = "Логин " + str(cgi.escape(login)) + " <font color = red>уже существует</font><br>"
        return True if len(str(login)) > 3 and dbusers.count() == 0 else False
    
    def checkPassword(self, password):
        return True if len(str(password)) > 4 else False

    def checkEmail(self, email, emailload = True, username = ''):
        mailtrue = True
        if email == '': return False
        try: 
            dbusers = db.GqlQuery("SELECT * FROM DBUser WHERE email = :email",
                                  email = cgi.escape(email))
            dbuser = dbusers.fetch(1)[0]
            if not (bool(emailload) and str(dbuser.login)==str(username)):
                mailtrue = False
        except:
            pass
        return True if dbusers.count() == 0 or mailtrue else False

    def get(self):
        self.insertTemplate('tpl_register.html', { 'title': 'Регистрация нового пользователя', 'button': 'Зарегистрировать', 'effect': False, 'load_username': True , 'check': True, 'action': False,  })
        self.drawPage()
        
    def post(self):
        #self.checkSession(self.request.headers.get('Cookie'))
        temp_uri = self.request.uri
        uri = temp_uri.split('/')
        if uri[-2]=='checklog':
            try:
                if not self.checkLogin(self.request.get('username')): 1/0
                self.response.out.write(self.answer)
            except:
                if(self.answer!=""):
                    self.response.out.write(self.answer)
                else:
                    self.response.out.write("<font color = red>В логине можно использовать только буквы латинского алфавита и цифры,<br>а его длинна должна быть не менее четырех символов</font>")
        elif uri[-2]=='checkmail':
            try:
                if not self.checkEmail(self.request.get('email'), self.request.get('emailload'), self.request.get('username')):
                    self.response.out.write("<font color = Red>Пользователь с таким адресом уже зарегистрирован</font>")
                    
                else:
                    1/0
            except:
                self.response.out.write("<font color = Green>Почта введена верно</font>")
        
        else:
            is_invited = False
            hash = str(uri[-1])
            invites = db.GqlQuery("SELECT * FROM DBInvite where used = :used", used=False)
            this_invite = DBInvite()
            for invite in invites:
                if invite.hash == hash:
                    is_invited = True
                    this_invite = invite
                    break
            
            if self.checkLogin(self.request.get('login')) and self.checkEmail(self.request.get('email')):
                this_invite.used = True
                dbuser = DBUser()
                dbuser.login = str(cgi.escape(self.request.get('login'))).lower()
                dbuser.password = hashlib.md5(self.request.get('password')).hexdigest()
                dbuser.name = cgi.escape(self.request.get('name'))
                dbuser.surname = cgi.escape(self.request.get('surname'))
                dbuser.email = cgi.escape(self.request.get('email'))
                confirmation = hashlib.md5(str(random.random())).hexdigest()
                dbuser.confirmation = confirmation
                dbuser.type = 'pending'
                
                if is_invited:
                    dbuser.access = 6
                else:
                    dbuser.access = 0
                
                this_invite.put()
                
                
#                try:
                
                subject = """[%s] Подтверждение регистрации""" % self.paramByName("name")

                body = """Спасибо за регистрацию на нашем сайте! Пожалуйста, активируйте свою учетную запись, следуя по ссылке:\n%s/confirm/%s\n__\nС уважением, администрация сайта.""" % (self.paramByName("url"), confirmation)
                PostOffice().append_to_queue(dbuser.put(), subject.decode("utf-8"), body.decode("utf-8"))
#                except:
#                    self.insertContent('Письмо на подверждение учетной записи не было отправлено<br>')
                self.showMessage('<h1>Регистрация успешно завершена<br>На ящик '+str(dbuser.email)+' было отправлено письмо для активации вашей учетной записи<br>Вы сможете зайти на сайт только после прохождения активации!</h1><br><a href=/>Вернуться на главную</a>')
                return
            else:
                self.insertContent("<h1>Данные введены неверно</h1>")
            self.drawPage("Регистрация")

from output_class import OutputClass
from google.appengine.api import mail
from google.appengine.ext import db
import hashlib, random

class PasswordRemind(OutputClass):
    
    url_handler = '/reminder/.*'
    
    def get(self):
        url = self.request.uri.split('/')[-2]
        if url=="reminder":
            self.insertContent("""<div style="padding: 10px;">Введите свой логин: 
    <form method=post>
        <input type=text value="" name="login">
        <input type=submit value="Ок">
    </form></div>""")
        else:
            dbQuery = db.GqlQuery("SELECT * FROM DBUser WHERE secret = :secret",
                                   secret = url)
            if dbQuery.count()==0 or url=="" or url=="null":
                self.insertContent("""Неверный запрос""")
            else:
                self.insertContent("""<form method="post" onsubmit = "return checkForm(this);" action='/reminder/""" + str(url) + """/'>
Введите новый пароль: <input name="password" id="password" type=password><br>Подтверждение пароля: <input id="passwordcheck" name="pascheck" type="password"><br><div id="passdiv"></div><br><input type=submit></form>""")
        self.drawPage()

    def post(self):
        url = self.request.uri.split('/')[-2]
        if url=="reminder":
            try:
                dbQuery = db.GqlQuery("SELECT * FROM DBUser WHERE login = :login",
                                      login = str(self.request.get('login')).lower())
                dbuser = dbQuery.fetch(1)
                user = dbuser[0]
                secret = hashlib.md5(str(random.random())).hexdigest()
                user.secret = secret
                mail.send_mail(sender = self.paramByName("email"), 
                               to = str(user.email), 
                               subject = "Запрос на изменение пароля", 
                               body="""Для того, чтобы ввести новый пароль, перейдите по ссылке:
                               """ + self.paramByName("url") + """/reminder/""" + str(secret) + """/""")
                user.put()
                self.insertContent("Письмо для продолжения операции изменения пароля было выслано на адрес, указанный при регистрации.")
            except:
                self.insertContent("Логина " + str(self.request.get('login')) + " не существует")
            self.drawPage()
        else:
            dbQuery = db.GqlQuery("SELECT * FROM DBUser WHERE secret = :secret",
                                  secret = url)
            dbuser = dbQuery.fetch(1)
            user = dbuser[0]
            user.secret=""
            user.password = hashlib.md5(self.request.get('password')).hexdigest()
            user.put()
            self.insertContent("Пароль успешно изменен")
            self.drawPage("Восстановление пароля")

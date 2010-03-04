from output_class import OutputClass
from google.appengine.ext import db
from google.appengine.api import mail

class RegisterConfirm(OutputClass):
    
    url_handler = '/confirm/.*'
    
    def sendEmailCheck(self, email, confirmation):
        our_email = self.paramByName("email")
        our_url = self.paramByName("url")
        mail.send_mail(sender=our_email,
              to=str(email),
              subject="[" + self.paramByName("name") + "] Подтверждение регистрации",
              body="""Спасибо за регистрацию на нашем сайте!  Пожалуйста, активируйте свою учетную запись, следуя по ссылке:
"""+our_url+"""/confirm/""" + str(confirmation) + """
__
С уважением, администрация сайта""")
        return email

    def get(self):
        confirmation = self.request.uri.split('/')[-1]
        try:
            userdb = db.GqlQuery("SELECT * FROM DBUser WHERE confirmation = :confirmation",
                                  confirmation = confirmation)
            userdb_temp = userdb.fetch(1)
            user = userdb_temp[0]
            user.confirmation=""
            user.type = "confirmed-email" if user.type == "pending-email" else "confirmed"
            user.put()
            self.insertContent('Активация учетной записи прошла успешно')
        except:
            self.insertContent('Ошибка активации')
        self.drawPage()

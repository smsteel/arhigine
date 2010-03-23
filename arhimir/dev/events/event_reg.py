# -*- coding: UTF-8 -*-﻿﻿
from google.appengine.ext import db
from google.appengine.ext.webapp import template
import cgi, random, hashlib
from output_class import OutputClass
from db_entities.event_anketa import DBEventAnketa
from db_entities.user import DBUser
from db_entities.event import DBEvent
from register_handler import RegisterHandler
from google.appengine.api import mail

class EventReg(OutputClass):
    """ guess who """
    
    url_handler = '/event/reg/.*'
    
    def get(self):
        """ Show all msg captions """
        self.checkSession(self.request.headers.get('Cookie'), False)
        self.insertMenu()
        eventid = int(self.request.uri.split('/')[-1])
        event = DBEvent.get_by_id(eventid)
        if self.Session['authorized']:
            users = db.GqlQuery("SELECT * FROM DBEventAnketa WHERE eventid = :eventid  AND userid = :userid",
                                eventid = eventid, 
                                userid = self.Session['userid'])
            
            if users.count() == 0:
                self.insertTemplate('tpl_reg_on_event.html', {'name' : self.Session['name'],
                                                                          'surname' : self.Session['surname'],
                                                                          'email' : self.Session['email'].encode("utf8"),
                                                                          'event_name'  : event.name.encode("utf8"),  })
            else:
                self.insertContent("Вы уже зарегистрировались на данное мероприятие!")
        else:
            self.insertTemplate('tpl_reg_on_event.html', { 'event_name'  : event.name.encode("utf8"), })
        self.drawPage(event.name.encode("utf8"))
        
    def post(self):
        self.checkSession(self.request.headers.get('Cookie'), False)
        event = int(self.request.uri.split('/')[-1])
        if not self.Session['authorized']:
            if self.request.get('name') != '' and self.request.get('surname') != '':
                user = db.GqlQuery("SELECT * FROM DBUser WHERE email = :email", 
                                   email = str(self.request.get('email')))
                if user.count() == 0:
                    newuser = DBUser()
                    newuser.name = self.request.get('name')
                    newuser.surname = self.request.get('surname')
                    newuser.login = str(cgi.escape(self.request.get('email'))).lower()
                    newuser.email = str(self.request.get('email'))
                    pwchars = "1234567890QWERTYUIOPASDFGHJKLZXCVBNMqwertyuiopasdfghjklzxcvbnm"
                    pwd = "".join(random.choice(pwchars) for x in range(8))
                    newuser.password = hashlib.md5(str(pwd)).hexdigest()
                    confirmation = hashlib.md5(str(random.random())).hexdigest()
                    newuser.confirmation = confirmation
                    newuser.type = 'pending-email'
                    newuser.put()
                    try:
                        
                        tpl_body = template.Template (self.paramByName("tpl_eventRegMailBody"))
                        mail_body = tpl_body.render(template.Context({
                                                                      "event_url": self.paramByName("url") + "/event/" +  str(event),
                                                                      "confirm": self.paramByName("url") + "/confirm/" + confirmation,
                                                                      "login": str(cgi.escape(self.request.get('email'))),
                                                                      "password": str(pwd)
                                                                      }))
                        
                        mail.send_mail(sender = self.paramByName("email"), 
                                       to = str(self.request.get('email')), 
                                       subject = self.paramByName("eventRegMailSubj"), 
                                       body = mail_body)
                        self.insertContent("""Вы зарегистрированны. На вашу почту была выслана регистрационная информация.<br>""")
                    except:
                        self.insertContent("""Вы зарегистрировались на мероприятие, но в процессе обработки произошел сбой.<br> 
                                    Если вы получили регистрационное письмо, авторизуйтесь с указанными там реквизитами.<br>
                                    Или <a href="/contacts">свяжитесь с администрацией</a>""")
            else:
                self.insertContent("Данные были введены неверно!")
                self.drawPage()
                return

        dbuser = db.GqlQuery("SELECT * FROM DBUser WHERE email = :email", email = str(cgi.escape(self.request.get('email'))).replace("%40", "@"))
        userid = self.Session['userid'] if self.Session['authorized'] else dbuser.fetch(1)[0].key().id()

        anketa = DBEventAnketa()
        anketa.userid = int(userid)
        anketa.eventid = int(event)
        anketa.name = db.Text(self.Session['name'], "utf_8") if self.Session['authorized'] else self.request.get('name')
        anketa.surname = db.Text(self.Session['surname'], "utf_8") if self.Session['authorized'] else self.request.get('surname')
        anketa.phone = self.request.get('phone')
        anketa.email = self.Session['email'] if self.Session['authorized'] else self.request.get('email')
        anketa.company = self.request.get('company')
        anketa.position = self.request.get('position')
#        anketa.payway = int(self.request.get('payway'))
        if self.request.get('is_portfolio'):
            anketa.is_portfolio = bool(int(self.request.get('is_portfolio')))
        anketa.additional = self.request.get('additional')
        if self.request.get('isarhitect'):
            anketa.isarhitect = bool(int(self.request.get('isarhitect')))
        anketa.put()
        self.showMessage(""" Ваша заявка принята! """)
        
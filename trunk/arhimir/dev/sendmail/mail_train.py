# -*- coding: UTF-8 -*-
from google.appengine.ext import webapp
from google.appengine.api import mail
from db_entities.sendmail.letter import Letter
from google.appengine.ext import db
from tools.tag_processor import tag_processor
from db_entities.user import DBUser

class MailTrain(webapp.RequestHandler):
    
    url_handler = '/system/mail_train/?'
    _step = 10
    
    def get(self):
        
        counter = 0
        
        letter_bag = Letter.gql("limit 10")
        if letter_bag.count(1):
            for letter in letter_bag:
                rcp = letter.to
                
                # нужен такой цикл, тк фор тупит при добавлении элементов
                while len(rcp) > 0:
                #for r in rcp:
                    self.send_letter(DBUser.get(rcp[0]).email, letter.subject, letter.body)
#                    rcp.remove(r)
                    rcp.pop(0)
                    counter += 1
                    print counter
                    if counter == self._step:
                        break
                if len(rcp) > 0:
                    letter.to = rcp
                    letter.put()
                else:
                    db.delete(letter)
                
    def send_letter(self, to, subject, body, sender="no.reply.arhimir@gmail.com"):
        try:
            mail.send_mail(sender, to, subject, body=tag_processor().del_tags(body.replace('<br />', '\n').replace('<br>', '\n')), html=body)
            return True
        except: return False
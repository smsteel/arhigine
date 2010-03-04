# -*- coding: UTF-8 -*-
from google.appengine.ext import webapp
from google.appengine.api import mail
from db_entities.sendmail.letter import Letter
from google.appengine.ext import db
from tools.tag_processor import tag_processor

class MailTrain(webapp.RequestHandler):
    
    url_handler = '/system/mail_train/?'
    
    def get(self):
        letter_bag = Letter.gql("limit 10")
        for letter in letter_bag:
            if self.send_letter(letter.to.email, letter.subject, letter.body):
                db.delete(letter)
            
    def send_letter(self, to, subject, body, sender="no.reply.arhimir@gmail.com"):
        try:
            mail.send_mail(sender, to, subject, body=tag_processor().del_tags(body), html=body)
            return True
        except: return False
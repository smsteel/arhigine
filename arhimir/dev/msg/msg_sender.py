# -*- coding: UTF-8 -*-
from db_entities.message import DBMSG
from db_entities.message_recipients import DBMSGRecipients
from db_entities.user import DBUser
from google.appengine.api import mail
from db_entities.custom_field import DBCustomField
from sendmail.post_office import PostOffice

class MSGSender():

    def send_msg(self, owner, recipient, content, caption = "None"):
        user = DBUser.gql("where login = :login", login = recipient)[0]
        recipientid = int(user.key().id())
        msg = DBMSG()
#        msg.owner = owner['id']
        msg.owner = owner
        msg.caption = caption if caption else "None"
        msg.content = content
        msgrecipient = DBMSGRecipients()
        msgrecipient.message = msg.put()
        msgrecipient.recipient = recipientid
        msgrecipient.put()
        if owner == -1:
            self.owner_login = "Admin"
            self.owner_name = "Администрация"
        else:
            dbowner = DBUser.get_by_id(owner)
            self.owner_login = dbowner.login
            self.owner_name = dbowner.name
        return self.__send_mail(recipient, user.email, self.owner_login, self.owner_name, content)
   
    def send_msg_mass(self, owner, gqlRecipients, content, caption):
        if owner == -1:
            self.owner_login = "Admin"
            self.owner_name = "Администрация"
        else:
            dbowner = DBUser.get_by_id(owner)
            self.owner_login = dbowner.login
            self.owner_name = dbowner.name
        msg = DBMSG()
        msg.owner = owner
        msg.caption = caption
        msg.content = content
        msg_key = msg.put()
        for recipient in gqlRecipients:
            msgrecipient =  DBMSGRecipients()
            msgrecipient.message = msg_key
            msgrecipient.recipient = int(recipient.key().id())
            msgrecipient.put()
            self.__send_mail(recipient.login, recipient, self.owner_login, self.owner_name, content)
    
    def __send_mail(self, recipient_login, recipient_email, owner_login, owner_name, content = ""):
        #try:
            urls = DBCustomField.gql("where type=3")
            our_url = urls[0].value.encode("utf8")
            emails = DBCustomField.gql("where type=2")
            our_email = emails[0].value.encode("utf8")
            subject = "[" + DBCustomField().getByName("name") + "] Личное сообщение"
            body = """Здравствуйте, """+str(recipient_login)+"""! \nВам личное сообщение! Прочитать можно на странице личных сообщений по адресу """+our_url+"""/msg/ \n""" + self._del_tags(content).encode("utf8")
            
#            if DBCustomField().getByName("mail_type") == "html":
##                html = content + unicode("""<p>_______<br/>От: <a href='http://www.runiver.net/users/""", 'utf_8') + str(owner_login) + "'>" + owner_name.encode("utf8") + unicode("""</a></p><p>не отвечайте на это сообщение<br/>ответить можно на сервере: """, "utf_8") + our_url + "/msg/</p>"
#                mail.send_mail(sender=our_email, to=str(recipient_email), subject = subject, body = body)#, html = html)
#            else:
            #mail.send_mail(sender=our_email, to=str(recipient_email), subject = subject, body = body)
            po = PostOffice()
            po.append_to_queue(recipient_email, subject, body)
            return True
        #except: return False
        
    def _del_tags(self, text):
        fixed_text = ''
        in_tag = False
        for letter in text:
            if letter == '<': in_tag = True
            if letter == '>':
                in_tag = False
                continue
            if in_tag: continue
            fixed_text += letter
        return fixed_text

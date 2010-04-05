#coding: UTF-8
from google.appengine.ext import db
from db_entities.message_recipients import DBMSGRecipients
from db_entities.user import DBUser
from output_class import OutputClass

class MSGHandler(OutputClass):
    """ guess who """
    
    url_handler = '/msg/?'
    
    def get(self):
        self.checkSession(self.request.headers.get('Cookie'))
        self.insertMenu()
        try:
            Incoming = self.getMsgCount('recipient')
        except: return
        self.insertTemplate('tpl_msg_menu.html', { 'incoming': Incoming, })
        self.drawPage()
    
    def getMsgCount(self, direction):
        msg = db.GqlQuery("SELECT * FROM DBMSGRecipients WHERE read = :read AND recipient = :userid",
                          read = False,
                          userid = self.Session['userid'])
        return str(msg.count())
    
    def getSentMSG(self, sender):
        """ Getting messages sender previously sent """
        msg = db.GqlQuery("SELECT * FROM DBMSG where owner = :owner",
                          owner = sender)
        if msg.count() == 0:
            self.insertContent('<div style="padding: 10px;">Нет исходящих сообщений</div>')
        else:
            self.insertContent('<table><tr><td width="150">Дата</td><td width="450">Тема</td><td width="250">Собеседник</td></tr>')
            for this_msg in msg:
                if this_msg.show_to_owner == False: continue
                msgrecipient = DBMSGRecipients.gql("where message = :message", message = this_msg)[0]
                recipient = DBUser.get_by_id(msgrecipient.recipient)
                template_values = { 'id'            : msgrecipient.key().id(),
                                    'date'          : msgrecipient.date.strftime("%d.%m.%y %H:%M"),
                                    'caption'       : this_msg.caption,
                                    'direction'     : 'для',
                                    'login'         : '<a href="/users/'+recipient.login+'">' + recipient.login +'</a>'
                                  }
                self.insertTemplate('tpl_msg.html', template_values)
            self.insertContent('</table>')
        self.drawPage("Личные сообщения")
        
    def getReceivedMSG(self, owner):
        """ Getting messages sender previously received """
        msg_r = db.GqlQuery("SELECT * FROM DBMSGRecipients where recipient = :recipient ORDER BY date DESC",
                          recipient = owner)
        if msg_r.count() == 0:
            self.insertContent('<div style="padding: 10px;">Нет входящих сообщений</div>')
        else:
            self.insertContent('<table><tr><td width="150">Дата</td><td width="450">Тема</td><td width="250">Собеседник</td></tr>')
            for msg in msg_r:
                owner_login = "Администрация"
                try:
                    owner = DBUser.get_by_id(msg.message.owner)
                    owner_login = '<a href="/users/'+owner.login+'">' + owner.login +'</a>'
                except: pass
                template_values = { 
                                    'id'            : msg.key().id(),
                                    'date'          : msg.date.strftime("%d.%m.%y %H:%M"),
                                    'caption'       : msg.message.caption,
                                    'direction'     : 'от',
                                    'login'      : owner_login
                                  } 
                self.insertTemplate('tpl_msg.html', template_values)
            self.insertContent('</table>')
        self.drawPage()
        
    def readMSG(self, id):
        """ Reading selected message """
        self.checkSession(self.request.headers.get('Cookie'))
        self.insertMenu()
        msg = DBMSGRecipients.get_by_id(id)
        if msg.message.owner != self.Session['userid'] and msg.recipient != self.Session['userid']:
            self.response.out.write("Это не ваше сообщение")
            return
        reply = False
        
        owner_login = "Администрация"
        try:
            owner = DBUser.get_by_id(msg.message.owner)
            owner_login = str(owner.login)
        except: pass
        
        if msg.recipient == self.Session['userid']:
            reply = True
            msg.read = True
            msg.put()              
        self.insertTemplate('tpl_msg_read.html', { 'caption' : msg.message.caption.encode("utf8"), 
                                                               'content' : msg.message.content.encode("utf8"),
                                                               'reply' : reply,
                                                               'owner' : owner_login })
        self.drawPage()

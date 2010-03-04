from msg_handler import MSGHandler

class MSGOutgoing(MSGHandler):
    """ guess who """
    
    url_handler = '/msg/outgoing/?'
    
    def get(self):
        """ Show all msg captions """
        self.checkSession(self.request.headers.get('Cookie'))
        try:
            self.insertMenu()
            self.getSentMSG(self.Session['userid'])
        except:
            self.response.out.write("Some error occured")

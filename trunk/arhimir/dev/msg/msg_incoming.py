from msg_handler import MSGHandler

class MSGIncoming(MSGHandler):
    """ guess who """
    
#    url_handler = '/msg/incoming/?'
    
    def get(self):
        """ Show all msg captions """
        self.checkSession(self.request.headers.get('Cookie'))
        try:
            self.insertMenu()
            self.getReceivedMSG(self.Session['userid'])
        except:
            self.response.out.write("Some error occured")


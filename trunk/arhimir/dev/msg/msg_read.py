from msg_handler import MSGHandler

class MSGRead(MSGHandler):
    """ guess who """
    
    url_handler = '/msg/read/.+'
    
    def get(self):
        self.checkSession(self.request.headers.get('Cookie'))
        msg_id = int(self.request.uri.split('/')[-1])
        try:
            self.readMSG(msg_id)
            pass
        except:
            self.response.out.write("Some error occured")


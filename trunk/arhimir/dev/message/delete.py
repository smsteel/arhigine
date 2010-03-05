from output_class import OutputClass
from message.handler import Handler
import sys

class Delete(OutputClass):
    
    url_handler = '/message/delete/?'
    access = 0
    
    def post(self):
        if not super(Delete, self).get(): return
        try:
            Handler().delete(self.request.get('messages').split(',')[:-1], self.Session['user_key'])
            self.response.out.write("success")
        except:
            self.response.out.write(sys.exc_info())
        
        
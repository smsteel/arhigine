from output_class import OutputClass
from message.handler import Handler
from tools.multipage import Multipage

class Outgoing(OutputClass):
    
    access = 0
    url_handler = '/message/outgoing/?'
    
    def get(self):
        if not super(Outgoing, self).get(): return 
        user = self.Session['user_key']
        
        messages = Handler().get_outgoing(user)
       
        multipage = Multipage(self.request.get('page'), messages, "/msg/incoming/")
        
        self.insertTemplate("message/outgoing.html", {
                                                        'messages' : multipage.getItems(),
                                                        'pages' : multipage.getPages()
                                                     })
        self.drawPage()
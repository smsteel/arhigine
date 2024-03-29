from output_class import OutputClass
from message.handler import Handler
from tools.multipage import Multipage

class Incoming(OutputClass):
    
    access = 0
    url_handler = '/message/incoming/?'
    
    def get(self):
        if super(Incoming, self).get(): self.insertMenu()
        else: return
        user = self.Session['user_key']
        
        messages = Handler().get_incoming(user)
       
        multipage = Multipage(self.request.get('page'), messages, "/msg/incoming/")
        
        self.insertTemplate("message/incoming.html", {
                                                        'messages' : multipage.getItems(),
                                                        'pages' : multipage.getPages()
                                                     })
        self.drawPage()
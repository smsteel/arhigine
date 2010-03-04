from output_class import OutputClass

class MainHandler(OutputClass):
    
    url_handler = '/'
    
    def get(self):
        self.redirect(self.paramByName("start"))

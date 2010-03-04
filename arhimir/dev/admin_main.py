from output_class import OutputClass
import os

class AdminMain(OutputClass):
    """ guess who """
    
    url_handler = '/admin/?'
    
    def get(self):
        """ Show all msg captions """
        self.checkSession(self.request.headers.get('Cookie'))
        self.insertMenu()
        self.insertTemplate('tpl_admin_main.html', { 
                                                        'access' : self.Session['access'],
                                                        'version' : os.getcwd().split('/')[-1].split('.')[0]
                                                   })
        self.drawPage()


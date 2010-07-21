# coding: utf-8

from output_class import OutputClass

class TagSearch(OutputClass):
    
    url_handler = '/googlesearch/?'
    
    def get(self):
        self.insertTemplate('search/googlesearch.html')
        self.drawPage("wf")
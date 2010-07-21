# coding: utf-8

from output_class import OutputClass
from db_entities.tags import DBTags
from tags.tag_handler3 import TagHandler

class TagSearch(OutputClass):
    
    url_handler = '/tager/?'
    
    def get(self):
        obj = TagHandler().get(['1'])
        pass
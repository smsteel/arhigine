#coding: UTF-8

#
#     NOT RECOMENDED TO USE!
#

from db_entities.photo_tags import DBPhotoTags
from output_class import OutputClass
from spe_tager import Tager
from google.appengine.ext import db
from google.appengine.api import memcache

class TagHandler(OutputClass):
    
    url_handler = '/tags/?'
    
    def get(self):
        
        data = self.generate()
        self.insertContent(data)
        self.drawPage()
        
    def generate(self):
        try:
            photos = db.Query(DBPhotoTags)
            all_tags = []
            for photo in photos:
                try:
                    tags = photo.tags.encode("utf8")
                    for tag in tags.split(","):
                        all_tags.append(tag)
                except: pass
            
            tager = Tager()
            data = tager.get_html_clouds(all_tags)
            
            memcache.delete("cloud", 0)
            memcache.add("cloud", data, 86400)
            return data
        except: return '<div style="width: 296px; float: left;">No tags</div>'
        
    def get_tags(self):
        ebali_nogami_eto_po_yaponski = memcache.get("cloud")
        if ebali_nogami_eto_po_yaponski is not None:
            return ebali_nogami_eto_po_yaponski
        else:
            return self.generate()
    
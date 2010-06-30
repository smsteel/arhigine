#coding: UTF-8
from output_class import OutputClass
from db_entities.banners.banner import Banner

class BannerAll(OutputClass):
    
    url_handler = '/banners/?'
    access = 8
    
    def get(self):
        if not super(BannerAll, self).get(): return
        self.checkSession(self.request.headers.get('Cookie'))
        self.insertMenu()
        
        banners = Banner.all()
        
        self.insertTemplate("banners/banners_list.html", {'banners': banners})
        self.drawPage()
    

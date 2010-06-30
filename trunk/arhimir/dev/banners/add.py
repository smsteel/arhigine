#coding: UTF-8
from output_class import OutputClass
from db_entities.banners.banner import Banner

class BannerAdd(OutputClass):
    
    url_handler = '/banner/add/?'
    access = 8
    
    def get(self):
        if not super(BannerAdd, self).get(): return
        self.checkSession(self.request.headers.get('Cookie'))
        self.insertMenu()
        self.insertTemplate("banners/banner.html")
        self.drawPage()
    
    def post(self):
        if not super(BannerAdd, self).get(): return
        self.checkSession(self.request.headers.get('Cookie'))
        banner = Banner()
        banner.name = self.request.get('name')
        banner.link = self.request.get('link')
        banner.image = self.request.get('image')
        banner.put()
        self.showMessage("Баннер добавлен")
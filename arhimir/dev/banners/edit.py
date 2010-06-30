#coding: UTF-8
from output_class import OutputClass
from db_entities.banners.banner import Banner

class BannerEdit(OutputClass):
    
    url_handler = '/banner/edit/.*'
    access = 8
    
    def get(self):
        if not super(BannerEdit, self).get(): return
        self.checkSession(self.request.headers.get('Cookie'))
        self.insertMenu()
        key = self.get_url_part(1)
        banner = Banner.get(key)
        self.insertTemplate("banners/banner.html", {'banner': banner})
        self.drawPage()
    
    def post(self):
        if not super(BannerEdit, self).get(): return
        self.checkSession(self.request.headers.get('Cookie'))
        key = self.get_url_part(1)
        banner = Banner.get(key)
        banner.name = self.request.get('name')
        banner.link = self.request.get('link')
        if self.request.get('image'):
            banner.image = self.request.get('image')
        banner.put()
        self.showMessage("Баннер изменен")
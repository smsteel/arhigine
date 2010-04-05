#coding: UTF-8
from google.appengine.api import images
from google.appengine.api import memcache
from google.appengine.ext import db
from output_class import OutputClass
from db_entities.news import DBNews

class NewsEdit(OutputClass):
    
    url_handler = '/news/edit/.*'
    access = 8
    
    def get(self):
        if not super(NewsEdit, self).get(): return
        self.checkSession(self.request.headers.get('Cookie'))
        id = int(self.request.uri.split('/')[-1])
        
        piece_of_news = DBNews.get_by_id(id)
        
        self.checkSession(self.request.headers.get('Cookie'))
        self.insertMenu()
        self.insertTemplate("tpl_news_add.html", { 'editor' : self.insertFckEdit(Name = "content",Value = piece_of_news.content, ToolbarSet = "Admin"),
                                                               'cap'    : piece_of_news.cap,
                                                               'preview': piece_of_news.preview, })
        self.drawPage()
    
    def post(self):
        if not super(NewsEdit, self).get(): return
        self.checkSession(self.request.headers.get('Cookie'))
        id = int(self.request.uri.split('/')[-1])
        piece_of_news = DBNews.get_by_id(id)
        
        piece_of_news.cap = self.request.get('cap')
        piece_of_news.preview = self.request.get('preview')
        piece_of_news.content = self.request.get('content')

        data = self.request.get('pic')
        if data:
            image = images.resize(data, 200, 200)
            piece_of_news.image = db.Blob(image)
        piece_of_news.put()
        memcache.delete("news4main")
        self.insertMenu()
        self.insertContent("Новость изменена!")
        self.drawPage()

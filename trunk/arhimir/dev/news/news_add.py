# -*- coding: UTF-8 -*-﻿﻿
from google.appengine.api import images
from google.appengine.ext import db
from google.appengine.api import memcache
from output_class import OutputClass
from db_entities.news import DBNews

class NewsAdd(OutputClass):
    
    url_handler = '/news/add/?'
    access = 8
    
    def get(self):
        if not super(NewsAdd, self).get(): return
        self.checkSession(self.request.headers.get('Cookie'))
        self.insertMenu()
        self.insertTemplate("tpl_news_add.html", { 'editor' : self.insertFckEdit("content", ToolbarSet = "Admin"), })
        self.drawPage()
    
    def post(self):
        if not super(NewsAdd, self).get(): return
        self.checkSession(self.request.headers.get('Cookie'))
        piece_of_news = DBNews()
        piece_of_news.userid = self.Session['userid']
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
        self.insertContent("Новость добавлена!")
        self.drawPage()

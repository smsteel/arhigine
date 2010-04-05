#coding: UTF-8
from google.appengine.ext import db
from output_class import OutputClass
from db_entities.page import DBPage

class PageList(OutputClass):
    
    url_handler = '/pages/?'
    access = 5
    
    def get(self):
        self.checkSession(self.request.headers.get('Cookie'), False)
        self.insertMenu()
        self.insertContent("<a href=/page/add/>Добавить страницу</a>")
        pages = db.Query(DBPage)
        self.insertContent("<div style='padding: 10px;'>")
        if pages.count() == 0:
            self.insertContent("Сейчас нет ни одной страницы.")
        for page in pages:
            self.insertContent('<table width=100% style="border-width: 1px; border-style: dashed;"><tr><td><a href="/page/edit/' + 
                               str(page.key().id()) + '">' + 
                               page.name.encode("utf8") + '</a><hr><font size=2>'+
                               page.title.encode("utf8") +
                               '</font><br><br></li></td></tr></table><br>')
        self.insertContent("</div>")
        
        self.drawPage()
    
    
#coding: UTF-8
from output_class import OutputClass
from db_entities.page import DBPage

class PageAdd(OutputClass):
    
    url_handler = '/page/add/?'
    access = 8
    
    def get(self):
        if not super(PageAdd, self).get(): return
        self.checkSession(self.request.headers.get('Cookie'))
        self.insertMenu()
        self.insertTemplate("tpl_page_add.html", { 'editor' : self.insertFckEdit("content", ToolbarSet = "Admin"), })
        self.drawPage()
    
    def post(self):
        if not super(PageAdd, self).get(): return
        self.checkSession(self.request.headers.get('Cookie'))
        
        page = DBPage()
        page.name = self.request.get('name')
        page.title = self.request.get('title')
        page.content = self.request.get('content')
        page.put()

        self.insertContent("Страница добавлена!")
        self.drawPage()

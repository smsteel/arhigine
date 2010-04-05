#coding: UTF-8
from output_class import OutputClass
from db_entities.page import DBPage

class PageEdit(OutputClass):
    
    url_handler = '/page/edit/.*'
    access = 8
    
    def get(self):
        if not super(PageEdit, self).get(): return
        self.checkSession(self.request.headers.get('Cookie'))
        self.insertMenu()
        
        id = int(self.request.uri.split('/')[-1])
        
        page = DBPage.get_by_id(id)
        
        self.insertTemplate("tpl_page_add.html", { 'editor' : self.insertFckEdit(Name = "content",Value = page.content, ToolbarSet = "Admin"),
                                                               'title'    : page.title,
                                                               'name': page.name, })
        self.drawPage()
    
    def post(self):
        if not super(PageEdit, self).get(): return
        self.checkSession(self.request.headers.get('Cookie'))
        id = int(self.request.uri.split('/')[-1])
        page = DBPage.get_by_id(id)
        
        page.title = self.request.get('title')
        page.name = self.request.get('name')
        page.content = self.request.get('content')
        page.userid = int(self.Session['userid'])

        page.put()
        
        self.insertMenu()
        self.insertContent("Страница изменена!")
        self.drawPage()

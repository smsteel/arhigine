#coding: UTF-8
from google.appengine.ext import db
from output_class import OutputClass

class PageHandler(OutputClass):
    """ guess who """
    
    url_handler = '/.+'
    
    def get(self):
#        page = DBPage()
#        page.name = 'about'
#        page.cap = 'О нас'
#        page.content = '<b>test page</b>'
#        page.put()
        title = ""
        name_from_url = self.request.path.split('/')[1]
        pages = db.GqlQuery("SELECT * FROM DBPage WHERE name = :name", name = name_from_url )
        if name_from_url == "page_not_found" and pages.count() == 0:
            self.insertContent("404. Страница не найдена.")
            self.drawPage()
            return
        elif name_from_url == "home" and pages.count() == 0:
            self.insertContent("Главной страницы не существует.")
            return
        if pages.count()>0:
            for page in pages:
                title = page.title.encode("utf8")
                self.insertContent(page.content.encode("utf8"))            
        else:
            #uri = self.request.uri
            #if uri[len(uri)-1] == '/': 
            self.redirect("/page_not_found")
            #else:
                #self.redirect(uri+'/')
        self.drawPage(title)

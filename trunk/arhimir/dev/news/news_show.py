#coding: UTF-8
from output_class import OutputClass
from db_entities.news import DBNews

class NewsShow(OutputClass):
    
    url_handler = '/news/.*'
    
    def get(self):
        self.checkSession(self.request.headers.get('Cookie'), False)
        self.insertMenu()
        
        parametres = self.get_from_url('news_id')
        
        
        object = DBNews.get_by_id(int(parametres.news_id))
        self.insertTemplate("tpl_news_show.html", { 'image'     : "<img src='/picture/2/"+str(parametres.news_id)+"'>",
                                                                'cap'       : object.cap.encode("utf8"),
                                                                'content'   : object.content.encode("utf8")})
        if self.Session['access'] >=8: 
            self.insertContent('<a href="/news/edit/%s">Редактировать</a>' % str(parametres.news_id))
        self.insertComments(object.key())
        self.drawPage("Просмотр новости :: "+object.cap.encode("utf8"))
#coding: UTF-8
from google.appengine.ext import db
from output_class import OutputClass
from db_entities.user import DBUser

class NewsList(OutputClass):
    
    url_handler = '/news/?'
    
    def get(self):
        self.checkSession(self.request.headers.get('Cookie'), True)
        self.insertMenu()
        
        news = db.GqlQuery("select * from DBNews order by date desc limit 5")
        self.insertContent("<div style='padding: 10px;'>")
#        if news.count() == 0:
#            self.insertContent("Сейчас нет ни одной новости.")
        for piece_of_news in news:
            u_class = DBUser()
            login = u_class.get_login_by_id(piece_of_news.userid)
            self.insertContent('<table width=100% style="border-width: 1px; border-style: dashed;"><tr><td><li>' + str(piece_of_news.date) +
                               ' | <a href="/news/' + 
                               str(piece_of_news.key().id()) + '">' + 
                               piece_of_news.cap.encode("utf8") + '</a>'+
                               '<font size=1> размещено '+
                               '<a href="/users/'+login+'">'+login+'</a>'+
                               '</font><hr><font size=2>'+
                               piece_of_news.preview.encode("utf8") +
                               '</font><br><br></li></td></tr></table><br>')
        self.insertContent("</div>")
        
        self.insertContent("<div style='padding: 10px;'><a href='/news_all/'>Архив новостей</a></div>")
        
        self.drawPage("Новости")
    
    
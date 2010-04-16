#coding: UTF-8
from google.appengine.ext import db
from output_class import OutputClass
from db_entities.user import DBUser

class NewsAll(OutputClass):
    
    url_handler = '/news_all/?'
    
    def get(self):
        if self.checkSession(self.request.headers.get('Cookie'), False):
            self.insertMenu()
        
        news = db.GqlQuery("select * from DBNews order by date desc")
        self.insertContent("<div style='padding: 10px;'>")
#        if news.count() == 0:
#            self.insertContent("Сейчас нет ни одной новости.")
        for piece_of_news in news:
            u_class = DBUser()
            login = u_class.get_login_by_id(piece_of_news.userid)
            self.insertContent('<table width="100%" style="border-width: "1px"; border-style: dashed;"><tr><td><li>' + str(piece_of_news.date.strftime("%d.%m.%Y")) +
                               ' | <a href="/news/' + 
                               str(piece_of_news.key().id()) + '">' + 
                               piece_of_news.cap.encode("utf8") + '</a>'+
                               '<font size="1"> размещено '+
                               '<a href="/users/'+login+'">'+login+'</a>'+
                               '</font><hr><font size=2>'+
                               piece_of_news.preview.encode("utf8") +
                               '</font><br><br></li></td></tr></table><br>')
        self.insertContent("</div>")
        
        self.drawPage("Архив новостей")
    
    
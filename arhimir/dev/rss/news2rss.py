from output_class import OutputClass
from db_entities.news import DBNews
from rss.rss_handler import RSS #a u shure?

class News2RSS(OutputClass):
    
    url_handler = "/news_rss"
    
    def get(self):
        news = DBNews().getItems(10)
        rss_ = RSS()
        
        for new in news:
            rss_.add_item(new['caption'], "ya.ru", new['preview'], new['date'])
            
        self.response.out.write(rss_.generate_rss())
        
        
            
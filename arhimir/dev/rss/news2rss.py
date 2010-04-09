from output_class import OutputClass
from db_entities.news import DBNews
from rss.rss_handler import RSS #a u shure?

class News2RSS(OutputClass):
    
    url_handler = "/news_rss"
    
    def get(self):
        self.response.headers['Content-Type'] = 'application/rss+xml'
        news = DBNews().getItems(10)
        rss_ = RSS()
        
        for new in news:
            rss_.add_item(new['caption'], "http://www.arhimir.ru/news/%s" % str(new['id']), new['preview'], new['truedate'], new['key'])
            
        self.response.out.write(rss_.generate_rss())
        
        
            
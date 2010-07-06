from output_class import OutputClass
from db_entities.news import DBNews
import datetime

class NewAppear(OutputClass):
    
    url_handler = '/news/appear/?'
    
    def get(self):
        news = DBNews.gql("where hiden = :h", h = True)
        for new in news:
#            try:
                if new.showdate <= datetime.datetime.today():
                    new.hiden = False
                    new.put()
#                    print 1
#            except:
#                print 2
from output_class import OutputClass
from db_entities.news import DBNews

class NewAppear(OutputClass):
    
    def get(self):
        news = DBNews.gql("where hiden = h", h = True)
        for new in news:
            pass
#coding: UTF-8
from output_class import OutputClass
from db_entities.stat_news import StatNews

class StatsNews(OutputClass):
    
    url_handler = '/admin/stats/news/?'
    access = 8
    
    def get(self):
        if not super(StatsNews, self).get(): return
        all = StatNews().all()
        counter = 0
        for stat in all:
            counter += stat.counter
        statistics = StatNews().all().order('-counter').fetch(10)
        self.insertMenu()
        self.insertTemplate('stat_news.html', {
                                               
            'stats' : statistics,
            'all' : counter
            
        })
        self.drawPage('Статистика просмотра новостей')
            
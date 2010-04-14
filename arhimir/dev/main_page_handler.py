#coding: UTF-8
from google.appengine.ext import db
from output_class import OutputClass
from tags.tag_handler import TagHandler
from db_entities.user import DBUser
from db_entities.event import DBEvent
from db_entities.conf import DBConf
from tools.arch_top import ArchTop
from google.appengine.api import memcache
import pickle, random

class MainPageHandler(OutputClass):
    
    url_handler = '/main/?'
    access = -1
    
    def get_news(self):
        spe_news = memcache.get("news4main")
        if not spe_news:
            try:
                spe_news = ''
                news = db.GqlQuery("select * from DBNews order by date desc LIMIT 5")
                spe_news+=("<div style='padding: 5px; margin-bottom: 50px;'>")
     
                counter = 0
                for piece_of_news in news:
                    counter += 1
                    if counter == 4:
                        spe_news += """
                        <div style="padding-left: 29px;">
                            <a href="http://fashionhome.ru/catalog/arcdes/13664.html">
                                <img src="/images/banners/dak_decor.gif" style="align: center;" />
                            </a>
                        </div>
                        """
                    u_class = DBUser()
                    login = u_class.get_login_by_id(piece_of_news.userid)
                    spe_news+=("""
                                <div style="float: left; width: 100%; border: 1px solid #fd9446; margin-bottom: 5px; margin-top: 5px; background-color: white;">
                                    <div style="padding: 4px;">
                                        <a href="/news/""" + str(piece_of_news.key().id()) + """\">
                                            """ +  piece_of_news.cap.encode("utf8") + """
                                        </a>
                                        <br>
                                        <font style="font-size: 10px; color: #333333;">
                                            Добавлена """ + str(piece_of_news.date.strftime("%d.%m.%Y")) + 
                                            """, <a href=\"/users/""" + login + """\">""" +
                                            login +      
                                            """</a>
                                        </font>
                                    </div>
                                    <div style="padding: 4px;">
                                        <font size=2>
                                            """ + piece_of_news.preview.encode("utf8") +   
                                            """
                                        </font>
                                        <br>
                                        <div style="text-align: right; margin-top: 8px;">
                                            <a style="font-size: 10px;" href="/news/""" + str(piece_of_news.key().id()) + """\">
                                                читать далее
                                            </a>
                                        </div>
                                    </div>
                                </div>
                               """)
                spe_news+=("</div>")
                memcache.add("news4main", spe_news, 3600)
            except: pass
        return spe_news

    def get(self):
        self.checkSession(self.request.headers.get('Cookie'), False)
        spe_news = self.get_news()
        
        th = TagHandler()
        tags = th.get_tags()
        
        events = memcache.get("events4main")
        if not events:
            events = []
            db_events = DBEvent.gql("where date >= :today", today = db.datetime.date.today())
            for event in db_events:
                if event.access <= self.Session['access']:
                    events.append( {'date' : event.date, 'name' : event.name, 'descr' : event.descr, 'id' : event.key().id() })
            memcache.add("events4main", pickle.dumps(events), 18000)
        else:
            events = pickle.loads(events)
        if not events:
            memcache.add("events4main", "no", 18000)
            
        confs = []
        try:
            confs = self.random_from_entity(DBConf, 3)
        except: pass
        
        at = None
        data = memcache.get('random_top')
        if data:
            at = pickle.loads(data)
        else:
            at = ArchTop().get_top()
            random.shuffle(at)
            memcache.add('random_top', pickle.dumps(at), 50)
        
        self.drawMainPage(self.insertScroll(), spe_news, tags, events, confs, at[0:5])
#        self.drawPage("Главная страница")
from google.appengine.ext import db
from db_entities.user import DBUser

class DBNews(db.Model):
    image = db.BlobProperty()
    cap = db.StringProperty()
    preview = db.TextProperty()
    content = db.TextProperty()
    userid = db.IntegerProperty()
    date = db.DateTimeProperty(auto_now_add = True)
    author = db.ReferenceProperty(DBUser)
    hiden = db.BooleanProperty(default = False)
    
    def getItems (self, count):
        news = []
        #db_news = db.GqlQuery("select * from DBNews")
        db_news = db.GqlQuery("select * from DBNews order by date desc").fetch(count)
        for item in db_news:
            news.append({
                         "id": item.key().id(),
                         "caption": item.cap,
                         "date": item.date.strftime("%d-%m-%Y") if item.date else "",
                         "sdate": item.date.strftime("%d.%m") if item.date else "",
                         "preview": item.preview,
                         "truedate": item.date.strftime("%a, %d %b %Y %H:%M:%S GMT") if item.date else "",
                         "key": item.key()
                         })
        return news
    

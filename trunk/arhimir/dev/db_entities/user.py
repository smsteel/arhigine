from google.appengine.ext import db
from google.appengine.api import memcache
import pickle

class DBUser(db.Model):
    login = db.StringProperty()
    password = db.StringProperty()
    name = db.StringProperty()
    surname = db.StringProperty()
    email = db.StringProperty()
    access = db.IntegerProperty(default = 0)
    type = db.StringProperty()
    confirmation = db.StringProperty()
    secret = db.StringProperty()
    about = db.TextProperty()
    date = db.DateTimeProperty(auto_now_add = True)
    twitter = db.StringProperty()
    livejournal = db.StringProperty()
    comments_count = db.IntegerProperty()
    reputation = db.IntegerProperty()

    def get_login_by_id(self, id):
        cache_name = "get_login_by_id_" + str(id)
        data = memcache.get(cache_name)
        if data:
            return pickle.loads(data)
        else:
            user = self.get_by_id(id)
            login = str(user.login)
            memcache.add(cache_name, pickle.dumps(login), 86400)
            return login
    
    def get_key_by_login(self, login):
        cache_name = "get_key_by_login_" + str(login)
        data = memcache.get(cache_name)
        if data:
            return db.Key(pickle.loads(data))
        else:
            key = db.GqlQuery("SELECT __key__ FROM DBUser WHERE login = :login", login=login)[0]
            memcache.add(cache_name, pickle.dumps(str(key)), 86400)
            return key
    
    def count_comments(self, key):
        if key:
            user = db.get(key)
            if user.comments_count:
                return user.comments_count
            else:
                cmt =  0
                for x_ in db.GqlQuery("select __key__ from DBComments where user = :user", user = key):
                    cmt += 1
                user.comments_count = cmt
                user.put()
            return cmt
        else:
            return 0
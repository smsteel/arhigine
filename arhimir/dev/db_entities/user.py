from google.appengine.ext import db

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

    def get_login_by_id(self, id):
        user = self.get_by_id(id)
        login = str(user.login)
        return login
    
    def get_key_by_login(self, login):
        return db.GqlQuery("SELECT __key__ FROM DBUser WHERE login = :login", login=login)[0]
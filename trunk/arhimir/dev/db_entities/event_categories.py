from google.appengine.ext import db

class DBEventCat(db.Model):
    name = db.StringProperty()
    descr = db.TextProperty()
    
    def get_categories(self):
        cat_list = []
        try:
            cats = self.all()
            for cat in cats:
                cat_list.append( {'id' : int(cat.key().id()), 'name' : cat.name.encode("utf8")} )
        except: pass
        return cat_list
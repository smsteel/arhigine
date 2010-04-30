from google.appengine.ext import db
from db_entities.user import DBUser

class Tag(db.Model):
    entity = db.ReferenceProperty()
    datetime = db.DateTimeProperty(auto_now_add = True)
    tag = db.StringProperty()
    user = db.ReferenceProperty(DBUser)
    
    def get_tags(self, entity):
        tags = []
        try:
            db_tags = db.Query("select * from Tags where entity = :entity", entity = entity)
            for tag in db_tags:
                tags.append(tag.tag)
        except:
            pass
        
        return tags
            
    
from google.appengine.ext import db

class DBFavorites(db.Model):
    userid = db.IntegerProperty()
    entityid = db.IntegerProperty()
    type = db.IntegerProperty()
    
    def add_to_list(self, userid, entity_id, type):
            self.userid = userid
            self.entityid = entity_id
            self.type = type
            self.put()

    def exists(self, userid, entity_id, type):
        objs = self.gql("where userid = :uid and entityid = :eid and type = :t", uid = userid, eid = entity_id, t = type)
        return bool(objs.count())
from google.appengine.ext import db

class DBMSG(db.Model):
    owner = db.IntegerProperty()
    caption = db.StringProperty()
    content = db.TextProperty()
    show_to_owner = db.BooleanProperty(default=True)
    
    def has_unread_msg(self, userid):
        try:
            msg = db.GqlQuery("SELECT * FROM DBMSGRecipients WHERE read = :read AND recipient = :uid",
                              read = False,
                              uid = userid)
            return bool(msg.count())
        except: return 0

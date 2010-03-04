from db_entities.counter import DBCounter
from google.appengine.ext import webapp
from sendmail.post_office import PostOffice
from google.appengine.ext import db 

class Counter(webapp.RequestHandler):
    
    url_handler = '/counter/'
    
    def get(self):
        po = PostOffice()
        po.append_to_queue(db.Key("agZydS1kZXZyDAsSBkRCVXNlchgCDA"), "test letter", "test")
#        # getting the url
#        uri = self.request.uri
#        uri = uri.split('/')
#        # parsing the url to get user and event id`s
#        try:
#            userid = int(uri[-1])
#            eventid = int(uri[-2])
#        except:
#            return
#        # trying to increase hits
#        try:
#            dbQuery = DBCounter.gql("WHERE userid = :userid AND eventid = :eventid",
#                                    userid = userid,
#                                    eventid = eventid)
#            dbCounters = dbQuery.fetch(1)
#            counter = dbCounters[0]
#            counter.hit += 1
#            counter.put()
#        #if not, creating a new entry in db
#        except:
#            dbCounter = DBCounter()
#            dbCounter.userid = userid
#            dbCounter.eventid = eventid
#            dbCounter.put()
#        # redirecting to image
#        self.redirect('/images/arhimir.gif')
                
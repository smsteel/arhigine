from db_entities.counter import DBCounter
from google.appengine.ext import webapp

class Visit(webapp.RequestHandler):
    
    url_handler = '/visit/.*'
    
    def get(self):
        
        uri = self.request.uri
        uri = uri.split('/')
        self.response.out.write(uri)

        try:
            userid = int(uri[-1])
            eventid = int(uri[-2])
        except:
            return
        
        try:
            dbQuery = DBCounter.gql("WHERE userid = :userid AND eventid = :eventid",
                                    userid = userid,
                                    eventid = eventid)
            dbCounters = dbQuery.fetch(1)
            counter = dbCounters[0]
            counter.visit += 1
            counter.put()
            self.redirect('/')
        except:
            return

        
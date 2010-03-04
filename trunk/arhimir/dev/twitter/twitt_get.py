import httplib, re

from google.appengine.api import memcache
from db_entities.twit import DBTwit

class TwittGet:
    
    _username = None
    def __init__(self, username):
        self._username = str(username)

    def get_last_twitt(self):

        if not self._username: return
        
        result = memcache.get("twitter_"+self._username)
        if result is None:
            
            try:
                twit = DBTwit.gql("where user = :user", user = self._username)[0]
                result = twit.twit
            except:
                pass
            
            try:
                conn = httplib.HTTPConnection("twitter.com", 80)
        
                conn.request("GET", "/statuses/user_timeline/"+self._username+".rss")
                
                con_result = conn.getresponse()
                
                data = con_result.read()
                
                conn.close()
      
                if data:
            
                    titles = []
        
                    titles = re.findall(":\s(.+?)</title>", data, re.DOTALL)
                    
                    new_twit = str(titles[0])
                    try:
                        twit = DBTwit.gql("where user = :user", user = self._username)[0]
                        twit.twit = new_twit
                        twit.put()
                    except:
                        twit = DBTwit()
                        twit.user = self._username
                        twit.twit = new_twit
                        twit.put()
                    
                    #memcache.delete("twitter_"+self._username, 0)
                    memcache.add("twitter_"+self._username, new_twit, 600)
            except:
                pass
        
        return "<a href='http://twitter.com/"+self._username+"' target='_blank'>"+result+"</a>"

#t = TwittGet("arhimir_ru")
#print t.get_last_twitt()

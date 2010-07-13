#coding: UTF-8
from google.appengine.ext import db
from output_class import OutputClass
import  pickle,operator
from google.appengine.api import memcache
from twitter.twitt_get import TwittGet

class UserList(OutputClass):
    """ guess who """
    
    url_handler = '/users/page/.*'
    
    """ Количество пользователей на странице """
    _users_per_page = 9
    
    _query = "SELECT * FROM DBUser where type='confirmed'"
    
    _memcache_name = "users_list"
    
    def get_users_count(self):
        return {
                    'non_confirmed_count'     :   db.GqlQuery("SELECT * FROM DBUser WHERE type!='confirmed'").count(),
                    'registered_count'  :   db.GqlQuery("SELECT * FROM DBUser WHERE type='confirmed'").count(),
                    'architects_count'  :   db.GqlQuery("SELECT * FROM DBUser WHERE access > 4 and access < 7").count()
               }
    
    def get(self):
        if self.checkSession(self.request.headers.get('Cookie'), False):
            self.insertMenu("users")
            
        data = memcache.get(self._memcache_name)
        users_serialized = []
        if data is None:
            users = db.GqlQuery(self._query)
            
#            for user in users:
#                twitt = False    
#                try:
#                    t = TwittGet(user.twitter.encode("utf8"))
#                    twitt = t.get_last_twitt()
#                except: pass
            for user in users:
                twitter = False    
                try:
                    twitter = user.twitter.encode("utf8")
                except: 
                    pass
                users_serialized.append({
                                            'id'        : user.key().id(),
                                            'login'     : user.login,
                                            'name'      : user.name,
                                            'surname'   : user.surname,
                                            'access'    : user.access,
                                            'registered' : user.date,
                                            'twitter'     : twitter,
                                         })
            users_serialized.sort(key=operator.itemgetter('registered'), reverse = True)
            memcache.add(self._memcache_name, pickle.dumps(users_serialized), 600)
        else:
            users_serialized = pickle.loads(data)
        page = int(self.get_url_part(1))
        
        pages = range(1, round(len(users_serialized)/9+1)) if len(users_serialized)%9 == 0 else range(1, round(len(users_serialized)/9+2))
        self.insertTemplate("tpl_multi_page.html", {
                                                     'users_list'       :   users_serialized[self._users_per_page*(page-1):self._users_per_page*page],
                                                     'pages_list'       :   pages[page-5 if page-5 > 0 else 0:page+5 if page+5 < len(pages)+1 else len(pages)+1],
                                                     'last_page'        :   len(pages),
                                                     'current_page'     :   page,
                                                     'users'            :   self.get_users_count(),
                                                     'you_admin'        :   True if self.Session['access'] > 9 else False
                                                   })
        self.drawPage("Список пользователей")

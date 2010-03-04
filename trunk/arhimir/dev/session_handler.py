import hashlib
import Cookie
import random
from db_entities.user import DBUser
from google.appengine.api import memcache
from google.appengine.ext import db
import pickle

class SessionHandler:
    
    def __generateHash(self):
        return hashlib.md5(str(random.random())).hexdigest()
    
    def __getSession(self, SessionCookie, doHash=False):
        if(SessionCookie.has_key('sid')):
            if not (SessionCookie.get('sid').value == 'sessiondestroyed'):
                return str(SessionCookie.get('sid').value)
        if doHash: return self.__generateHash()
        else: return False
    
    def __SessionRead(self, SessionID):
        try:
            Session = pickle.loads(memcache.get("Session_"+SessionID))
            Session['user_key'] = db.Key(Session['user_key'])
            return Session
        except:
            Session = { 'authorized' : False, 'sid' : '', 'login' : '', 'access' : -1, 'name' : '', 'surname' : '', 'userid' : -1, 'user_key' : False }
            return Session
    
    def __SessionWrite(self, Session):
        try:
            dbuser = DBUser.get_by_id(int(Session['userid']))
            Session['name'] = dbuser.name.encode("utf8")
            Session['surname'] = dbuser.surname.encode("utf8")
            Session['email'] = str(dbuser.email)
            Session['access'] = int(dbuser.access)
            Session['type'] = str(dbuser.type)
            Session['user_key'] = str(dbuser.key())
            try:
                memcache.delete("Session_"+str(Session['sid']), 0)
            except: pass
            data = pickle.dumps(Session)
            memcache.add("Session_"+str(Session['sid']), data, 604800)
        except:
            pass
        
    def createSession(self, UserID, myCookie, login):
        SessionCookie = Cookie.SimpleCookie(myCookie)
        SessionID = self.__getSession(SessionCookie, True)
        Session = {'sid'        : SessionID,
               'userid'         : UserID, 
               'authorized'     : True,
               'login'       : login
                }
        self.__SessionWrite(Session) 
        return Session
    
    def getSessionInfo(self, myCookie):
        SessionCookie = Cookie.SimpleCookie(myCookie)
        SessionID = self.__getSession(SessionCookie)
        Session = self.__SessionRead(SessionID)
        return Session
    
    def destroySession(self, SessionID):
        memcache.delete("Session_"+SessionID, 0)
    
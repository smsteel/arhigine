from google.appengine.api import memcache
from db_entities.gallery_object import DBGalleryObject
from db_entities.user import DBUser
from db_entities.user_picture import DBAvatara
import pickle

class ArchTop():
    
    def get_top(self):
#        print 1
        arhs = []
        data = memcache.get("arch_top")
        if data is not None:
            arhs = pickle.loads(data)
#            print 2
        else:
            data = memcache.get("sorted_objects_v2")
#            print 3
            if not data: return arhs
            o_list = pickle.loads(data)[0:25]
            objects = []
            for object in o_list:
                objects.append(DBGalleryObject.get_by_id(object))
            
            rating = {}
    
            u = DBUser()
            
            obj_k = 100.0
            for object in objects:
                try:
                    rating[int(object.userid)] += 1.0*obj_k
                except:
                    rating[int(object.userid)] = 1.0*obj_k
                obj_k /= 1.1
            
            rate = sorted(rating.items(), key = lambda(k,v): (v,k), reverse=True)
            
            for entity in rate[:25]:

                # lets check if user has a photo
                if not DBAvatara().get_by_userid(entity[0]):
                    continue
                
                slovar = {'id': entity[0], 'login' : str(u.get_login_by_id(entity[0]))}
                arhs.append( slovar )
            memcache.add("arch_top", pickle.dumps(arhs), 3600)
        return arhs

from google.appengine.api import memcache
from db_entities.gallery_object import DBGalleryObject
from db_entities.user import DBUser
import pickle, operator

class ArchTop():
    
    def get_top(self):
        arhs = []
        data = memcache.get("arch_top")
        if data is not None:
            arhs = pickle.loads(data)
        else:
            data = memcache.get("sorted_objects_v2")
            if not data: return arhs
            o_list = pickle.loads(data)
            objects = []
            for object in o_list:
                objects.append(DBGalleryObject.get_by_id(object))
            
            rating = {}
    
    #            cnt = 0
            u = DBUser()
    #            while 1:
    #                slovar = {'id': objects[cnt].userid, 'login' : str(u.get_login_by_id(objects[cnt].userid))}
    #                if not slovar in arhs: 
    #                    arhs.append( slovar )
    #                cnt += 1
    #                if len(arhs)==5: break
    #            
    #            return arhs
    
            obj_k = 100.0
            for object in objects:
                try:
                    rating[int(object.userid)] += 1.0*obj_k
                except:
                    rating[int(object.userid)] = 1.0*obj_k
                obj_k /= 1.1
            
            rate = sorted(rating.items(), key = lambda(k,v): (v,k), reverse=True)
            
    #        for key,value in rating.items():
    #            rate.append( { 'key': key,
    #                           'value' : value })
    #            
    #        #rating2 = rate.sort(key=operator.itemgetter('value'), reverse = False)[:5]
            for entity in rate[:5]:
                slovar = {'id': entity[0], 'login' : str(u.get_login_by_id(entity[0]))}
                arhs.append( slovar )
            memcache.add("arch_top", pickle.dumps(arhs), 3600)
        return arhs

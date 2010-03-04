from google.appengine.ext import webapp
from google.appengine.ext import db
from google.appengine.ext.webapp import template
from google.appengine.api import memcache
import pickle

class AjaxScroll(webapp.RequestHandler):
    
    url_handler = '/scroll/.*'
    __nonAjax_preload = 6
    
    def _getSortedObjects(self):
        data = memcache.get("sorted_objects_v2")
        if not data:
            ratings = db.GqlQuery("SELECT * FROM DBGalleryObjectRate")
            objects = {}
            for rating in ratings:
                if int(rating.object) in objects:
                    objects[int(rating.object)] += 1 if bool(rating.is_nice) else -1
                else:
                    objects[int(rating.object)] = 1 if bool(rating.is_nice) else -1
            obj_good = []
            for objectid, rating in sorted(objects.items(), key=lambda (k,v): (v,k), reverse = True):
                if rating > 0:
                    obj_good.append(objectid)       
            data = pickle.dumps(obj_good)
            memcache.add("sorted_objects_v2", data, 36000)
        return pickle.loads(data)

    def get(self):
        if self.request.get("load"):
            id = int(self.request.get("load"))
            object = self._getSortedObjects()[id]
            self.response.out.write(str(object))

    def render(self):
        thumbs = ""
        for object in self._getSortedObjects()[:self.__nonAjax_preload]:
            thumbs += """
            <div class="tmbs" onclick='window.location = "/objects/""" + str(object) + """\"'>
            

                <span style="margin-left: 7px; margin-top: 7px; display:block; width:200px; height:200px; background-image:url(/picture/200/crop/0/""" + str(object) + """);"></span>
                

                
            </div>"""
        return template.render('templates/tpl_scroll.html', { 'thumbs': thumbs,
                                                              'nonAjax': self.__nonAjax_preload,
                                                              'objects_count': len(self._getSortedObjects()) })

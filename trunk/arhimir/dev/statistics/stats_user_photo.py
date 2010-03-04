from output_class import OutputClass
from google.appengine.ext import db
from google.appengine.api import memcache
import operator, pickle
    
class StatsUserPhoto(OutputClass):
    
    url_handler = '/admin/stats/gallery/photo/?'
    access = 8
    
    def get(self):
        if not super(StatsUserPhoto, self).get(): return
        self.insertMenu()
        data = memcache.get("user_photo_stats")
        if data is None:
            users = db.GqlQuery("SELECT * FROM DBUser WHERE access > 4")
            users_photo_stats = []
            for user in users:
                albums = db.GqlQuery("SELECT * FROM DBAlbum WHERE userid = :userid", userid = int(user.key().id()))
                photolen = 0
                photoscount = 0
                for album in albums:
                    photos = db.GqlQuery("SELECT * FROM DBPhoto WHERE albumid = :albumid", albumid = int(album.key().id()))
                    photoscount += int(photos.count())
                    for photo in photos:
                        photolen += len(photo.image_big)
                        photolen += len(photo.image_small)
                user_photo_stats = { 
                                     'photos_size'      : round(float(photolen)/1024.0/1024.0, 1), 
                                     'photos_count'     : photoscount,
                                     'user_login'       : str(user.login),
                                     'user_id'          : user.key().id(),
                                     'user_highlight'   : True if user.access > 7 else False
                                   }
                if photoscount: users_photo_stats.append(user_photo_stats)
            users_photo_stats.sort(key=operator.itemgetter('photos_size'), reverse = True)
            memcache.add("user_photo_stats", pickle.dumps(users_photo_stats), 86400)
            self.insertTemplate('tpl_stats_user_photo.html', { 
                                                              'user_photo_stats' : users_photo_stats
                                                              })
        else:
            stats = pickle.loads(memcache.get("user_photo_stats"))
            self.insertTemplate('tpl_stats_user_photo.html', { 
                                                              'user_photo_stats' : stats
                                                              })
        self.drawPage()


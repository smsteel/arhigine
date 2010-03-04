import random, hashlib
from db_entities.gallery_object import DBGalleryObject
from db_entities.album import DBAlbum
from db_entities.photo import DBPhoto
from db_entities.user import DBUser
from output_class import OutputClass
from google.appengine.ext import db
from google.appengine.api import images

class AdminAlbumAdd(OutputClass):
    
    url_handler = '/admin/album/add/.*'
    access = 5
    
    def get(self):
        if super(AdminAlbumAdd, self).get():
            id = 0
            try:
                id = int(self.request.uri.split('/')[-1])
            except: pass
            objects = db.Query(DBGalleryObject)
            if self.Session['access'] < 8:
                if objects.count()!=0:
                    objects.filter("userid =", self.Session['userid'])
                    objects.order("name")
            else:
                if objects.count()!=0: objects.order("userid")
            options = ''
            if objects.count()!=0:
                for object in objects:
                    owner = DBUser.get_by_id(int(object.userid))
                    own = """(Объект """ + owner.login.encode("utf8") + """) """
                    selected = ""
                    if int(object.key().id()) == id:
                        selected = "selected"
                    options += """<option """ + selected + """ value=""" + str(object.key().id()) + """>""" + own + object.name.encode("utf8") + """</option>"""
            self.insertMenu()
            albums = db.Query(DBAlbum)
            albums.filter("objectid =", -1)
            albums.filter("userid =", self.Session['userid'])
            if albums.count() == 0:
                self.album = DBAlbum()
            else:
                photos_to_delete = DBPhoto.gql("where albumid = :aid", aid = int(albums[0].key().id()))
#                photos_to_delete = db.Query(DBPhoto)
#                photos_to_delete.filter("albumid =", int(albums[0].key().id()))
                db.delete(photos_to_delete)
                self.album = DBAlbum.get_by_id(int(albums[0].key().id()))
            secret = str(hashlib.md5(str(random.random())).hexdigest())
            self.album.name = secret
            self.album.objectid = -1
            self.album.userid = self.Session['userid']
            self.album.put()
            albums = db.Query(DBAlbum)
            albums.filter("name =", secret)
            
            self.insertContent("Album ID: " + str(int(albums[0].key().id())))
#            statistics = db.GqlQuery("SELECT * FROM __Stat_Kind__ WHERE kind_name = 'DBPhoto'")
#            global_stat = stats.GlobalStat.all().get()
            self.insertTemplate("tpl_admin_album_add.html", { 'options' : options,
                                                              'albumid' : int(albums[0].key().id()),
#                                                              'bytes' : global_stat.bytes,
                                                              'isadmin' : True if self.Session['access'] == 10 else False,
                                                            })
            self.drawPage()
        
        
    def post(self):
        if super(AdminAlbumAdd, self).get():
            self.response.headers['Content-Type'] = "text/html"
            if int(self.request.get("isphoto"))==1:
                try:
                    photo = DBPhoto()
                    photo.albumid = int(self.request.get("albumid"))
                    photo.tags = ""
                    secret = str(hashlib.md5(str(random.random())).hexdigest())
                    photo.comment = "secret" + secret
                    image = images.Image(self.request.get('pic'))
                    if (image.width < 400 and image.height < 400) or image.width > 1024 or image.height > 768:
                        self.response.out.write("size")
                        return
                    image_resized = images.Image(images.resize(image._image_data, width=130, output_encoding = images.JPEG)) if image.height >= image.width else images.Image(images.resize(image._image_data, height=130, output_encoding = images.JPEG))
                    image_cropped = images.crop(image_resized._image_data, 0.0, 0.0, float(130)/float(image_resized.width), 1.0, images.JPEG) if image_resized.height == 130 else images.crop(image_resized._image_data, 0.0, 0.0, 1.0, float(130)/float(image_resized.height), images.JPEG)
                    photo.put()
                    photos = DBPhoto.gql("where comment = :cmt", cmt = "secret" + secret)
                    id = str(photos[0].key().id())
                    edphoto = DBPhoto.get_by_id(int(id))
                    edphoto.comment = "none"
                    edphoto.image_small = db.Blob(image_cropped)
                    edphoto.image_big = db.Blob(image._image_data)
                    edphoto.put()
                    self.response.out.write(id)
                except:
                    self.response.out.write("size")
            else:
                if int(self.request.get("deletephoto"))==1:
                    try:
                        photo = DBPhoto.get_by_id(int(self.request.get("photoid")))
                        db.delete(photo)
                        self.response.out.write("deleted")
                    except:
                        self.response.out.write("not deleted")
                else:
                    try:
                        album = DBAlbum.get_by_id(int(self.request.get("albumid")))
                        album.objectid = int(self.request.get("objectid"))
                        object = DBGalleryObject.get_by_id(int(self.request.get("objectid")))
                        album.userid = int(object.userid)
                        album.name = self.request.get("name")
                        album.put()
                        self.response.out.write("added")
                    except:
                        self.response.out.write("not added")
#                self.redirect('/msgbox/albumaddtrue')
#            i = 0
#            album = DBAlbum()
#            secret = str(hashlib.md5(str(self.Session['userid']+random.random())).hexdigest())
#            album.name = secret #self.request.get("name")
#            album.objectid = int(self.request.get("object"))
#            album.userid = self.Session['userid']
#            album.put()
#            albums = db.Query(DBAlbum)
#            albums.filter("name =", secret)
#            albums.fetch(1)
#            album = DBAlbum.get_by_id(int(albums[0].key().id()))
#            album.name=self.request.get("name")
#            while(self.request.get('pic'+str(i))):
#                if str(self.request.get('pic'+str(i))) != "deleted":
#                    try:
#                        photo = DBPhoto()
#                        image = images.Image(self.request.get('pic'+str(i)))
#                        image_resized = images.Image(images.resize(image._image_data, width=130, output_encoding = images.JPEG)) if image.height >= image.width else images.Image(images.resize(image._image_data, height=130, output_encoding = images.JPEG))
#                        image_cropped = images.crop(image_resized._image_data, 0.0, 0.0, float(130)/float(image_resized.width), 1.0, images.JPEG) if image_resized.height == 130 else images.crop(image_resized, 0.0, 0.0, 1.0, float(130)/float(image_resized.height), images.JPEG)
#                        photo.image_small = db.Blob(image_cropped)
#                        if (image.width < 400 and image.height < 400) or image.width > 1024 or image.height > 768:
#                            self.insertContent("Фотография не должна быть больше 1024x768 пикселей, но хотя бы одна сторона фотографии должна быть больше 400 пикселей")
#                            self.drawPage()
#                            return
#                        photo.image_big = db.Blob(image._image_data)
#                        #photo.image_big = db.Blob(images.resize(self.request.get('pic'), 1024, 768))
#                        photo.tags = self.request.get('tags'+str(i)) if self.request.get('tags'+str(i)) else ""
#                        photo.albumid = int(albums[0].key().id())
#                        photo.put()
#                    except:
#                        photos = db.Query(DBPhoto)
#                        photos.filter("albumid =", int(albums[0].key().id()))
#                        db.delete(photos)
#                        db.delete(album)
#                        self.redirect('/msgbox/albumaddbig')
#                        return
#                i += 1
#            album.put()
#            self.redirect('/msgbox/albumaddtrue')

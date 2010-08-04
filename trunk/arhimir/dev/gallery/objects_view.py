#coding: UTF-8
from google.appengine.ext import db
from db_entities.gallery_object import DBGalleryObject
from db_entities.album import DBAlbum
from db_entities.photo import DBPhoto
from db_entities.user import DBUser
from db_entities.gallery_object_rate import DBGalleryObjectRate
from output_class import OutputClass
from db_entities.favorites import DBFavorites

class ObjectsView(OutputClass):
    
    url_handler = '/objects/.*'
    
    def get(self):
        if self.checkSession(self.request.headers.get('Cookie'), False):
            self.insertMenu()
        id = int(self.request.uri.split('/')[-1])
        object = DBGalleryObject.get_by_id(id)
        
        """ count rating """
        votes = DBGalleryObjectRate.gql("where object = :o_key", o_key = id)
        rating = 0
        for vote in votes:
            if vote.is_nice:
                rating += 1
            else:
                rating -= 1
        if rating <0:
            rating = 0 
        can_vote = DBGalleryObjectRate().still_can_vote(self.Session['userid'], id)
        obj = DBGalleryObjectRate.gql("where object = :o_key and voter = :userid", o_key = id, userid = self.Session['userid'])
        my_vote = bool(obj[0].is_nice) if not can_vote else False
        user = DBUser.get_by_id(int(object.userid))

        albums = db.Query(DBAlbum)
        albums.filter("objectid =", id)
        albumhtml = ""
        for album in albums:
            albumhtml += """
                <div class="main">
        
                <div style="width: 100%; float: left;">
                    <div style="float: left;"><img src="/images/border_left_up.png" /></div>
                    <div style="float: right;"><img src="/images/border_right_up.png" /></div>
                </div>
                
                <div style="padding-left: 20px; margin-right: 20px; font-size: 18px;">Альбом <a href=\"/album/""" + str(album.key().id()) + """\">\"""" + album.name.encode("utf8") + """\"</a></div>
                <div style="padding-left: 20px; padding-top: 10px;">
                <a href=\"/album/""" + str(album.key().id()) + """\">Нажмите, чтобы посмотреть весь альбом</a>
                </div>
                <div style="padding-left: 20px; margin-right: 20px; padding-top: 10px;" class="triggers">
            """
            photos = DBPhoto.gql("where albumid = :albumid limit 0,6", albumid = int(album.key().id()))
            photohtml = ""
            for photo in photos:
                photohtml += """<div style="float: left; width: 136px; margin-right: 10px;"><a href="/picture/watermark/4/""" + str(photo.key().id()) + """\"><img src="/picture/3/""" + str(photo.key().id()) + """\" /></a></div>"""
            albumhtml += photohtml + """
                        <div style="clear: both; margin: 20px 20px 0px 0px; padding-top: 20px;">Комментариев к альбому: """ + str(album.comments_count if album.comments_count else 0) + """</div>
                        </div>
                        
                        <div style="width: 100%; float: left;">
                            <div style="float: left;"><img src="/images/border_left_down.png" /></div>
                            <div style="float: right;"><img src="/images/border_right_down.png" /></div>
                        </div>
                        
                </div>"""
#            self.insertContent("""<li><a href='/album/""" + str(album.key().id()) + """'>""" + album.name.encode("utf8") + """</a></li>""")
        show_rating = False
        if self.Session['access'] >= 0:
            show_rating = True
        self.insertContent("</div>")
        
        new_f = DBFavorites()
        in_fav = new_f.exists(self.Session['userid'], id, 1)

        self.insertTemplate("tpl_object_view.html", { 
                                                      'objectname' : object.name.encode("utf8"), 
                                                      'objectid' : str(id),
                                                      'objectdesription' : object.description.encode("utf8").split("\n")[1][1:-1] if object.description and len(object.description.encode("utf8").split("\n"))>1 else "</p>",
                                                      'ownerlogin' : user.login.encode("utf8"),
                                                      'ownername' : user.name.encode("utf8"),
                                                      'ownersurname' : user.surname.encode("utf8"),
                                                      'albums' : albumhtml,
                                                      'rating' : rating,
                                                      'show_rating' : show_rating,
                                                      'delobject' : True if int(object.userid) == self.Session['userid'] or self.Session['access'] >= 8 else False,
                                                      'can_vote': can_vote,
                                                      'my_vote': my_vote,
                                                      'in_fav' : in_fav,
                                                      } )
        self.drawPage("Объект :: " + object.name.encode("utf8"))
        
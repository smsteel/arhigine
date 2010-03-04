# -*- coding: UTF-8 -*-﻿﻿
from output_class import OutputClass
from db_entities.album import DBAlbum
from db_entities.photo import DBPhoto
from db_entities.user import DBUser
from db_entities.gallery_object import DBGalleryObject
from db_entities.photo_tags import DBPhotoTags
from google.appengine.ext import db
from db_entities.favorites import DBFavorites

class AlbumView(OutputClass):

    url_handler = '/album/.*'

    def get(self):
        self.checkSession(self.request.headers.get('Cookie'), False)
        id = int(self.request.uri.split('/')[-1])
        self.insertMenu()
        album = DBAlbum.get_by_id(id)
        object = DBGalleryObject.get_by_id(int(album.objectid))

        photos = db.Query(DBPhoto)
        photos.filter("albumid =", id)
        
        user = DBUser.get_by_id(int(object.userid))
            
        
        
#        self.insertContent("""
#        
#        <div id="triggers">
#        """)
        photos_html = ""
        for photo in photos:
#            taghtml = ""
#            try:
#                tags = photo.tags.encode("utf8").split(", ")
#                for tag in tags:
#                    taghtml += tag + """, """
##                    taghtml += """<form style="float: left;" id="search""" + tag + """" action="/search/" method="post"><input type="hidden" name="find" value=""" + tag + """><span class="tag" id="hover" onclick="tagsubmit(\"""" + tag + """\");">""" + tag + """</span></form>"""
#            except: 
#                taghtml = "Тэги отсутствуют"\
            dbtags = DBPhotoTags.gql("where imageid = :imageid", imageid = int(photo.key().id()))
            tags = dbtags[0].tags.encode("utf8") if dbtags.count() != 0 else """Тэги отсутствуют"""
            photos_html += """
    <div style="float: left; width: 136px; margin-right: 10px;">
    <a href="/picture/watermark/4/""" + str(photo.key().id()) + """" title=\"""" + tags + """\">
        <img src="/picture/3/""" + str(photo.key().id()) + """" />
    </a>
"""
#            try:
#                tags = photo.tags.encode("utf8").split(", ")
#                for tag in tags:
#                    self.insertContent("""<div style="float: left;"><form style="float: left;" id="search""" + tag + """" action="/search/" method="post"><input type="hidden" name="find" value=""" + tag + """><span class="tag" id="hover" onclick='$("#search""" + tag + """").submit()'>""" + tag + """</span></form></div>""")
#            except: pass
            try:
                if(self.Session['access'] >=8  or self.Session['userid'] == int(album.userid) ):
                    photos_html += """<div style="float: left; margin-left: 4px;"><span id="hover" class="tag" onclick='window.location = "/edit_photo/%s";'>Редактировать</span></div>""" % str(str(photo.key().id()))
                    photos_html += """<div style="float: left; font-size: 10px; margin-left: 4px;">Photo ID: """ + str(photo.key().id()) + """</div>"""
            except: pass
            photos_html += "</div>"
            
        options = ''
        if self.Session['access'] > 5:
            objects = db.Query(DBGalleryObject)
            if self.Session['access'] < 8:
                objects.filter("userid =", self.Session['userid'])
                if objects.count()!=0: objects.order("name")
            else:
                objects.order("userid")
            
            for objecti in objects:
                owner = DBUser.get_by_id(int(objecti.userid))
                own = """(Объект """ + owner.login.encode("utf8") + """) """
                selected = ""
                if int(objecti.key().id()) == int(album.objectid):
                    selected = "selected"
                options += """<option """ + selected + """ value=""" + str(objecti.key().id()) + """>""" + own + objecti.name.encode("utf8") + """</option>"""
            
        
        new_f = DBFavorites()
        in_fav = new_f.exists(self.Session['userid'], id, 2)
        
        self.insertTemplate("tpl_album_view.html", { 'albumid' : str(id),
                                                                 'isadmin' : True if self.Session['access'] >= 8 else False, 
                                                                 'name' : album.name.encode("utf8"),
                                                                 'connected' : object.name.encode("utf8"),
                                                                 'objectid' : str(object.key().id()),
                                                                 'ownerlogin' : user.login.encode("utf8"),
                                                                 'ownername' : user.name.encode("utf8"),
                                                                 'ownersurname' : user.surname.encode("utf8"),
                                                                 'addphoto' : True if int(object.userid) == self.Session['userid'] or self.Session['access'] >= 8 else False,
                                                                 'photos' : photos_html,
                                                                 'options' : options,
                                                                 'in_fav' : in_fav,
                                                                  })
        self.drawPage("Альбом :: "+album.name.encode("utf8"))
        
    def post(self):
        album = DBAlbum.get_by_id(int(self.request.get("albumid")))
        album.objectid = int(self.request.get("objectid"))
        album.put()
        self.redirect("/album/" + str(self.request.get("albumid")))
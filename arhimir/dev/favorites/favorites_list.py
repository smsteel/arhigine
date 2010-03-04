# -*- coding: UTF-8 -*-
from output_class import OutputClass
from db_entities.favorites import DBFavorites
from db_entities.gallery_object import DBGalleryObject
from db_entities.album import DBAlbum

class FavoritesList(OutputClass):

    url_handler = '/favorites/?'
    access = 0

    def get(self):
        if not super(FavoritesList, self).get():
            self.showMessage("У вас недостаточно прав для выполнения этого действия")
            return
        """ получаем type """
        
        self.insertMenu()
        
        user_id = self.Session['userid']
        
        favs = DBFavorites.gql("where userid = :uid", uid = user_id)
        favorites = []
        fav_objects = []
        for fav in favs:
            if fav.type == 1:
                obj = DBGalleryObject.get_by_id(int(fav.entityid))
                fav_objects.append({
                                    'type_cap' : "объекты",
                                    'type_val'  : 0,
                                    'type_str'  : 'objects',
                                    'id'    : fav.entityid,
                                    'name'  : obj.name.encode("utf-8"),
                                 })
            elif fav.type == 2:
                obj = DBAlbum.get_by_id(int(fav.entityid))
                fav_objects.append({
                                    'type_cap' : "альбомы",
#                                    'type_val'  : -1,
                                    'type_str'  : 'album',
                                    'id'    : fav.entityid,
                                    'name'  : obj.name.encode("utf-8"),
                                 })
                
        favorites.append(fav_objects)
        self.insertTemplate("tpl_favorites_list.html", { 'favorites' : favorites }) 
        self.drawPage("Список избранного")
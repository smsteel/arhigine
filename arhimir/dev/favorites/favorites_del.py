# -*- coding: UTF-8 -*-
from output_class import OutputClass
from db_entities.favorites import DBFavorites
from google.appengine.ext import db

class FavoritesDel(OutputClass):

    url_handler = '/favorites/del/.*'
    access = 0

    def get(self):
        if not super(FavoritesDel, self).get():
            self.showMessage("У вас недостаточно прав для выполнения этого действия")
            return
        
        """ получаем ID объекта """
        entity_id = int(self.request.uri.split('/')[-1])
        
        """ получаем id юзера """
        user_id = self.Session['userid']
        
        got_f = DBFavorites.gql("where entityid = :eid", eid = entity_id)
        type = int(got_f[0].type)
        if got_f[0].userid == user_id: 
            db.delete(got_f[0])
        
        if type == 2:
            href = "/album/%i" % entity_id
        elif type == 1:
            href = "/objects/%i" % entity_id
        self.showMessage("Удалено из избранного!<br><a href='%s'>Вернуться</a>" % href)
        
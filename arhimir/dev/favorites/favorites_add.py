# -*- coding: UTF-8 -*-
from output_class import OutputClass
from db_entities.favorites import DBFavorites

class FavoritesAdd(OutputClass):

    url_handler = '/favorites/add/.*'
    access = 0

    def get(self):
        if not super(FavoritesAdd, self).get():
            self.showMessage("У вас недостаточно прав для выполнения этого действия")
            return
        """ получаем ID объекта """
        entity_id = int(self.request.uri.split('/')[-1])
        """ получаем type """
        type = int(self.request.uri.split('/')[-2])
        """ получаем id юзера """
        user_id = self.Session['userid']
        
        new_f = DBFavorites()
        try:
            if new_f.exists(user_id, entity_id, type):
                self.showMessage("Объект уже в избранном!")
                return
            new_f.add_to_list(user_id, entity_id, type)
            if type == 2:
                href = "/album/%i" % entity_id
            elif type == 1:
                href = "/objects/%i" % entity_id
            self.showMessage("Добавленое в избранное!<br><a href='%s'>Вернуться</a>" % href)
        except:
            self.showMessage("Что-то не получилось =(")
        
        
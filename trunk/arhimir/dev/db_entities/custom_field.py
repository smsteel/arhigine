# -*- coding: UTF-8 -*-

from google.appengine.ext import db

class DBCustomField(db.Model):
    type = db.IntegerProperty()
    value = db.TextProperty()
    name = db.StringProperty()

    param_set = {}
    param_n = {}
    param_set["name"] = param_n[1] = {
                   "type":1,
                   "name":"name",
                   "caption":"Краткое название портала",
                   "value":"Не задано"
                   }
    param_set["email"] = param_n[2] = {
                   "type":2,
                   "name":"email",
                   "caption":"e-mail адрес для отправки уведомлений",
                   "value":"admin@localhost"
                   }
    param_set["url"] = param_n[3] = {
                   "type":3,
                   "name":"url",
                   "caption":"url сайта с http://",
                   "value":"http://localhost"
                   }
    param_set["tpl"] = param_n[4] = {
                   "type":4,
                   "name":"tpl",
                   "caption":"путь к шаблонам",
                   "value":"templates/"
                   }
    param_set["start"] = param_n[5] = {
                   "type":5,
                   "name":"start",
                   "caption":"стартовая страница",
                   "value":"/main/"
                   }
    param_set["eventRegMailSubj"] = param_n[6] = {
                   "type":6,
                   "name":"eventRegMailSubj",
                   "caption":"Тема письма, отправляемого при регистрации на событие",
                   "value":"[Название портала] Регистрация на мероприятие"
                   }
    param_set["tpl_eventRegMailBody"] = param_n[7] = {
                   "type":7,
                   "name":"tpl_eventRegMailBody",
                   "caption":"Шаблон содержания письма, отправляемого при регистрации на событие",
                   "value":"""Вы зарегистрировались на мероприятие на портале и вам была выделена учетная запись:
                                       Ваш логин для входа в систему: {{login}}
                                       Ваш пароль для входа в систему: {{password}}
                                       Чтобы активировать учетную запись откройте эту страницу: {{confirm}}
                                       Карточка события: {{event_url}}
                                       ___
                                       С уважением, администрация портала"""
                   }
    param_set["new_arch"] = param_n[8] = {
                   "type":8,
                   "name":"new_arch",
                   "caption":"Сообщение новым архитекторам",
                   "value":"Grats! U have a lot of right now!"
                   }
    param_set["url_watermark"] = param_n[9] = {
                   "type":9,
                   "name":"url_watermark",
                   "caption":"Где лежит картинка с водяным знаком для фото в альбомах",
                   "value":"http://7.latest.ru-dev.appspot.com/images/watermark.png"
                   }
#    param_set["mail_type"] = param_n[10] = {
#                   "type":10,
#                   "name":"mail_type",
#                   "caption":"Тип писем(text/html)",
#                   "value":"text"
#                   }
    

#    def getByType (self, type):
#        try:
#            rows = self.gql("where type=:type", type = type)
#            return rows[0].value.encode("utf8")
#        except:
#            return self.param_n[type]["value"]
    
    def getByName (self, name):
        try:
            rows = self.gql("where name=:name", name = name)
            return rows[0].value.encode("utf8")
        except:
            return self.param_set[name]["value"]

# coding=utf-8

from output_class import OutputClass
from db_entities.order import DBOrder
from msg.msg_sender import MSGSender
from message.handler import Handler

""" Класс-обработчик заказов """
class OrderHandler(OutputClass):
    
    url_handler = '/order/.*'
    
    """ отсылает архитектору личное сообщение с заказом """
    def inform(self, arch, msg_text):
#        msgsend = MSGSender()
        content = msg_text.decode("utf8")
        caption = "3AKA3!"
        try:
            Handler().send(self.Session['user_key'], [arch], caption, content)
#            msgsend.send_msg(-1, arch, content, caption)
            return True
        except:
            return False
    
    """ выводим форму заказа """
    def get(self):
        self.insertTemplate("tpl_order.html")
        self.drawPage("Оформить заказ")
        
    """ Добавляем заказ в БД и уведомляем всех о нем """
    def post(self):
        
        """ А все ли у нас хорошо? """
        try:
        
            """ получаем ID архитектора, для которого регистрируем заказ """
            arch = str(self.request.uri.split('/')[-1])
            
            """ получаем инфу из поста """
            fio = self.request.get('fio')
            phone = self.request.get('phone')
            email = self.request.get('email')
            type = self.request.get('type')
            square = self.request.get('square')
            misc = self.request.get('misc')
            
            """ проверяем все ли нам прислали """
            if not (fio and phone and email and type and square and misc):
                self.insertContent("Необходимо заполнить все поля формы!")
                self.drawPage()
                return
                                
            """ Записываем наш заказ в БД """
            order = DBOrder()
            order.arch = arch
            order.fio = fio
            order.phone = phone
            order.email = email
            order.type = type
            order.square = square
            order.misc = misc
            order.status = "none"
            order.put()
            
            msg_text = "Заказ от %s<br>" % fio.encode("utf8")
            msg_text += "Для %s<br>" % arch.encode("utf8")
            msg_text += "Телефон %s<br>" % phone.encode("utf8")
            msg_text += "Email %s<br>" % email.encode("utf8")
            msg_text += "Тип объекта %s<br>" % type.encode("utf8")
            msg_text += "Площадь %s<br>" % square.encode("utf8")
            msg_text += "Дополнительно %s<br>" % misc.encode("utf8")
            
            self.inform(arch, msg_text)
            self.inform("oleg", msg_text)
            self.inform("spe", msg_text)

            
            """ Выводим сообщение о том, что все ОК """
            self.insertContent("Спасибо за заказ!")
            self.drawPage("Оформление заказа")
            
            """ А если нехорошо? """
        except:
            self.insertContent("Что-то пошло не так! Если ошибка повторяется, свяжитесь с администрацией портала!")
            self.drawPage("Оформление заказа")
            
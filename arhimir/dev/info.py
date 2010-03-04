from output_class import OutputClass
from db_entities.gallery_object import DBGalleryObject
class Info(OutputClass):

    url_handler = '/msgbox/.*'

    __messages = { "msgtrue" : "Сообщение отправлено!",
                   "msgfalse" : "Сообщение не отправлено!",
                   "objectaddtrue" : "Объект успешно добавлен",
                   "objectedittrue" : "Объект успешно изменен",
                   "albumaddtrue"   : "Альбом успешно добавлен",
                   "albumaddbig"    : "Слишком большой размер фотографии. Максимально допустимым размером является 1 Мб.",
                   "albumdeleted"   : "Альбом удален",
                   "approvesend"    : "Заявка отправлена! Наш менеджер свяжется с Вами по телефону в ближайшие дни.",
                   "approvefail"    : "Заявку отправить не удалось. Попробуйте чуть позже!"
                  }
    
    def get(self):
        self.checkSession(self.request.headers.get('Cookie'), False)
        self.insertMenu()
        uri = self.request.uri.split('/')[-1]
        output = self.__messages[uri]
        if uri == "objectaddtrue":
            object = DBGalleryObject.gql("order by date desc limit 0,1")
            output += """<br><a href="/admin/album/add/""" + str(object[0].key().id()) + """\">Добавить фотоальбом к этому объекту</a>"""
            output += """<br><a href="/admin/objects/add/">Добавить еще объект</a>"""
            output += """<br><a href="/admin/objects/">Перейти в управление объектами</a>"""
        self.insertTemplate('tpl_messagebox.html', { 'content' : output } )
        self.drawPage()
        
    def post(self):
        self.checkSession(self.request.headers.get('Cookie'), False)
        self.insertMenu()
        self.insertTemplate('tpl_messagebox.html', { 'content' : self.request.get("message_text") })
        self.drawPage()

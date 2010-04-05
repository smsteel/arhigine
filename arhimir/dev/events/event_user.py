#coding: UTF-8
from output_class import OutputClass
from db_entities.event_anketa import DBEventAnketa
from db_entities.user import DBUser

class EventUser(OutputClass):
    
    url_handler = '/event/user/.*'
    
    def get(self):
        self.checkSession(self.request.headers.get('Cookie'), False)
        self.insertMenu()
        anketaid = self.request.uri.split('/')[-1]
        useranketa = DBEventAnketa.get_by_id(int(anketaid))
        user = DBUser.get_by_id(int(useranketa.userid))
#        payway = {  0   : 'Бесплатно',
#                    1   : 'Безналичный рассчет',
#                    2   : 'Наличными с курьером',
#                    3   : 'Web-Money' }
        self.insertTemplate('tpl_user_anketa.html', { 'name'            : useranketa.name.encode("utf8"),
                                                                  'surname'         : useranketa.surname.encode("utf8"),
                                                                  'company'         : useranketa.company.encode("utf8"),
                                                                  'phone'           : useranketa.phone.encode("utf8"),
                                                                  'position'        : useranketa.position.encode("utf8"),
#                                                                  'payway'          : payway[int(useranketa.payway)],
                                                                  'is_portfolio'    : useranketa.is_portfolio,
                                                                  'isarhitect'      : useranketa.isarhitect,
                                                                  'additional'      : useranketa.additional.encode("utf8"),
                                                                  'login'       : user.login.encode("utf8"), 
                                                                   })
        self.drawPage()
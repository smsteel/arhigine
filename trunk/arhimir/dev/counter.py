# -*- coding: UTF-8 -*-
#from db_entities.counter import DBCounter
#from google.appengine.ext import webapp
#from sendmail.post_office import PostOffice
#from google.appengine.ext import db 
#
#class Counter(webapp.RequestHandler):
#    
#    url_handler = '/counter/'
#    
#    def get(self):
#        po = PostOffice()
#        po.append_to_queue(db.Key("agZydS1kZXZyDAsSBkRCVXNlchgCDA"), "test letter", "test")
##        # getting the url
##        uri = self.request.uri
##        uri = uri.split('/')
##        # parsing the url to get user and event id`s
##        try:
##            userid = int(uri[-1])
##            eventid = int(uri[-2])
##        except:
##            return
##        # trying to increase hits
##        try:
##            dbQuery = DBCounter.gql("WHERE userid = :userid AND eventid = :eventid",
##                                    userid = userid,
##                                    eventid = eventid)
##            dbCounters = dbQuery.fetch(1)
##            counter = dbCounters[0]
##            counter.hit += 1
##            counter.put()
##        #if not, creating a new entry in db
##        except:
##            dbCounter = DBCounter()
##            dbCounter.userid = userid
##            dbCounter.eventid = eventid
##            dbCounter.put()
##        # redirecting to image
##        self.redirect('/images/arhimir.gif')
#                


from output_class import OutputClass
from sendmail.post_office import PostOffice
from db_entities.user import DBUser

class Counter(OutputClass):
    
    url_handler = '/counter/'
    
    def get(self):
        subject = "Тренинг 'Эффективное общение с клиентом'"
        body = """Уважаемые архитекторы!

19 мая проект "Архимир" проводит бизнес-тренинг для архитекторов и дизайнеров интерьеров.

Тренинг «Эффективное общение с клиентом»

Дата 19 мая

Место проведения улица Малая Ордынка, дом 23

Продолжительность тренинга 1 день с 11 до 19

Бизнес — тренер Ольга Болтович (информация о тренере http://www.arhimir.ru/forum/topic/687001)

Организатор: Проект «Архимир»

Программа тренинга

    * Как преодолеть барьеры в начале разговора?
    * Как произвести благоприятное впечатление на клиента и создать атмосферу доверия? (техники установления контакта)
    * Как грамотно построить переговоры (этапы переговоров)?
    * Как удерживать инициативу и управлять процессом переговоров?
    * Как быстро получать необходимую информацию от клиента (правила постановки вопросов)?
    * Как слушать и слышать клиента (техники активного слушания)?

Ответы на эти  и другие вопросы можно получить на тренинге. Также участники смогут в практических упражнениях потренировать применение основополагающих переговорных техник.

Стоимость тренинга 3000 рублей

Для участия в тренинге необходимо внести предоплату в размере 500 рублей. Оставшуюся стоимость в размере 2500 рублей необходимо оплатить на тренинге. В случае отказа от тренинга менее чем за 2 дня, предоплата не возвращается.

Внести предоплату и получить пригласительный билет Вы можете в офисе компании "Арнэт", по адресу улица пятницкая д. 2.

Зарегистрироваться на тренинг можно по телефону 642-47-43

        """
        # get arhs
        arhs = DBUser.gql("where access = 6")
        for arh in arhs:
            PostOffice().append_to_queue(arh, subject.decode('utf-8'), body.decode('utf-8'))
            
        self.showMessage("ok")
        
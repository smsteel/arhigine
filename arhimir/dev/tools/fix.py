### -*- coding: UTF-8 -*-
##
##from db_entities.user import DBUser
##from output_class import OutputClass
##from google.appengine.ext import db
##from db_entities.news import DBNews
##from db_entities.event import DBEvent
##
##class fix(OutputClass):
##    
###    url_handler = '/fix'
##    
##    def get(self):
##        
##        news = DBEvent.all()
##        for new in news:
##            new.author = DBUser.get_by_id(new.userid)
##            new.put()
##       
###        users_ = [7051,12041,13015,13016,14001,15015,15033,15040,15056,15069,16011,16018,16031,19003,19008]
###        users = DBUser.get_by_id(users_)
###        for user in users:
###            user.date = db.datetime.datetime.today()
###            user.put()
#
#import cgi
#
#def prepare(text, tags = ['a', 'img']):
#        
#        prepared_text = cgi.escape(text)
#        
#        for tag in tags:
#            topic_text = ""
#            prepared_text = prepared_text.replace("&lt;/"+tag+"&gt;", "</"+tag+">").replace("&lt;"+tag+"", "<"+tag+" ")
#            r_flag = False
#            s_flag = 0
#            
#            for letter in prepared_text:
#        
#                if letter == '<':
#                    r_flag = True
#                    s_flag = 0
#                          
#                if r_flag:
#                    if s_flag == 3:
#                        if letter == ';':
#                            s_flag = 0
#                            r_flag = False
#                            topic_text += '>'
#                            continue
#                        else: s_flag = 0
#                    if s_flag == 2:
#                        if letter == 't':
#                            s_flag = 3
#                        else: s_flag = 0
#                    if s_flag == 1:
#                        if letter == 'g':
#                            s_flag = 2
#                        else: s_flag = 0
#                    if s_flag == 0:
#                        if letter == '&':
#                            s_flag = 1
#                     
#                if s_flag == 0: 
#                    topic_text += letter
#                
#        return topic_text
#    
#    
#text = """
#<a href="http://ya.ru">yandex</a>
#<b href="http://ya.ru">yandex</b>
#<img src="omg"></img>
#"""
#
#print prepare(text)   
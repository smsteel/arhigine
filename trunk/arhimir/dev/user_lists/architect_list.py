#coding: UTF-8
from user_lists.user_list import UserList

class ArhitectList(UserList):
    """ guess who """
    
    url_handler = '/users/arhitectors/.*'
    
    _query = "SELECT * FROM DBUser where access>4 and access<7"
    
    _memcache_name = "arhitect_list"

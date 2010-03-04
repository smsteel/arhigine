# -*- coding: UTF-8 -*-﻿﻿
from user_lists.user_list import UserList

class ArhimirList(UserList):
    """ guess who """
    
    _query = "SELECT * FROM DBUser where access>7"
    
    _memcache_name = "arhimir_list"
    
    url_handler = '/users/arhimir/.*'

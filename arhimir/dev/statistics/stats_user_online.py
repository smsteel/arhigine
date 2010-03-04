from output_class import OutputClass
from google.appengine.api import memcache
from google.appengine.ext import db
from db_entities.user import DBUser
from db_entities.stat_daily_users import DBDailyUsers
from datetime import timedelta 
from datetime import date

class StatsUserOnline(OutputClass):
    
    url_handler = '/admin/stats/online/?'
    access = 8
    
    def get(self):
        if not super(StatsUserOnline, self).get(): return
        users = db.Query(DBUser)
        users_list = []
        for user in users:
            users_list.append(str(user.key().id()))
        users_list = memcache.get_multi(users_list, "user_activity_")
        users_online = []
        for key, value in users_list.iteritems():
            users_online.append({ 
                                 'user_id' : int(key),
                                 'login'  : str(value),
                                })
        dbusers_daily_online = DBDailyUsers.gql("WHERE date = :date", date = db.datetime.date.today())
        users_daily_online = []
        for user in dbusers_daily_online:
            users_daily_online.append({
                                        'user_id'    : user.userid,
                                        'login'     : user.login,
                                      })
        users_per_days = DBDailyUsers.gql("WHERE date > :date", date = date.today() + timedelta(days=-30))
        activity_stats = {}
        for user in users_per_days:
            if user.date in activity_stats:
                activity_stats[user.date] += 1
            else:
                activity_stats[user.date] = 1
        act_stats = []
        act_dates = activity_stats.keys()
        act_dates.sort()
        for stat_date in act_dates:
            act_stats.append(str(activity_stats[stat_date]*5))
        self.insertMenu()
        self.insertTemplate("tpl_stats_user_online.html", { 
                                                            'users_online' : users_online,
                                                            'users_daily_online' : users_daily_online,
                                                            'act_dates' : act_dates,
                                                            'act_stats' : act_stats,
                                                            'act_max' : act_stats.index(max(act_stats)),
                                                            'act_min' : act_stats.index(min(act_stats)),
                                                          })
        self.drawPage()

from db_entities.banners.banner import Banner
from db_entities.banners.iteration import BannerIter

class Handler():
    
    def get_banner_by_name(self, name):
        return Banner.gql("where name = :name", name = name)[0]
    
    def get_banner_by_number(self, number):
        return Banner.all()[number]
    
    def count_banners(self):
        return Banner.all().count()
    
    def get_iter(self):
        iter = 0
        try:
            iter = BannerIter.all()[0]
            iter.number += 1
            iter.put()
            return iter.number
        except:
            iter = BannerIter()
            iter.put()
            return 0
        
    def next_banner(self):
        iter = self.get_iter()
        all = self.count_banners()
        if not all:
            return {}
        ban = self.get_banner_by_number(iter % all)
        
        form_banner = {'link': ban.link, 'key': ban.key()}
        return form_banner
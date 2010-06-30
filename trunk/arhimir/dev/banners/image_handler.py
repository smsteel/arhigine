from output_class import OutputClass
from db_entities.banners.banner import Banner

class BannerImage(OutputClass):
    
    url_handler = '/banner/show/.*'
    
    def get(self):
        key = self.get_url_part(1)
        ban = Banner.get(key)
        
        self.response.headers['Content-Type'] = 'image/jpeg'
#        self.response.headers['Expires'] = "Thu,01 Jan 2020 00:00:01 GMT"
#        self.response.headers['Cache-Control'] = "public"
        
        self.response.out.write(ban.image)
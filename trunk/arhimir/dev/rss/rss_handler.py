from google.appengine.ext.webapp import template

class RSS():
    
    _items = []
    
    def add_item(self, title, link, description, pubdate):
        self._items.append(
                           {
                             'title': title,
                             'link': link,
                             'description': description,
                             'pubdate': pubdate,
                           }
                           )
        
    def generate_rss(self):
        return template.render("rss/rss.html", {'items': self._items})
        
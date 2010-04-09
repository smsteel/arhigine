from google.appengine.ext.webapp import template

class RSS():
    
    _items = []
    
    def add_item(self, title, link, description, pubdate, key):
        self._items.append(
                           {
                             'title': title,
                             'link': link,
                             'description': description,
                             'pubdate': pubdate,
                             'key': key,
                           }
                           )
        
    def generate_rss(self):
        return template.render("rss/rss.html", {'items': self._items})
        
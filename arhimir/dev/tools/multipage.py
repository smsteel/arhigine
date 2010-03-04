class Multipage():
    
    items_per_page = 10
    current_page = 1
    list = None
    url = ""

    def __init__(self, current_page, list, url):
        if current_page:
            self.current_page = int(current_page)
        self.list = list
        self.url = url + "&" if url.find("?") > 0 else url + "?"

    def getPages(self):
        pages = { 
                    'list' : range(1, len(self.list) // self.items_per_page + 2)[0 if self.current_page < 5 else self.current_page - 5:self.current_page + 5],
                    'current_page' : self.current_page,
                    'last_page' : len(self.list) // self.items_per_page + 1,
                    'url' : self.url
                }
        return pages
    
    def getItems(self):
        return self.list[self.items_per_page * (self.current_page - 1):self.items_per_page * (self.current_page - 1) + self.items_per_page]

from db_entities.tag.tag import Tag

class tag_handler():
    
    def get_tags(self, entity):
        return Tag().get_tags(entity)
    
    def insert_tags(self, tags, user, entity):
        for tag in tags:
            db_tag = Tag()
            db_tag.tag = tag
            db_tag.user = user
            db_tag.entity = entity
            db_tag.put()
    
    def generate_tag_form(self, entity):
        pass
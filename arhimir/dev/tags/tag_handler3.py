from db_entities.tag.tag import TagsList

class TagHandler():
    
    def add(self, user, object, **tags):
        pass
    
    def get(self, tags):
        tags_lists = TagsList.all()
        for tag in tags:
            tags_lists = tags_lists.filter('tags IN', tags)
        return tags_lists
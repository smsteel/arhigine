from db_entities.sendmail.letter import Letter

class PostOffice:
    
    def __init__(self):
        pass
    
    def append_to_queue(self, to, subject, body):
#        try:
            new_letter = Letter()
            new_letter.to = to
            new_letter.subject = subject
            new_letter.body = body
            new_letter.put()
            return True
#        except: return False
    


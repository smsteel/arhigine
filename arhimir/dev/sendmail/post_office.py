from db_entities.sendmail.letter import Letter

class PostOffice:
   
    def append_to_queue(self, to, subject, body):
        new_letter = Letter()
        
        #check if to is a list
        if type(to) != type([]):
            new_to = [to]
            to = new_to
        
        new_letter.to = to
        new_letter.subject = "[arhimir.ru]"+subject
        new_letter.body = body
        new_letter.put()

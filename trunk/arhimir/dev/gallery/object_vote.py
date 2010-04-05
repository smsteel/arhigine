#coding: UTF-8
from output_class import OutputClass
from db_entities.gallery_object_rate import DBGalleryObjectRate

class ObjectVote(OutputClass):

    url_handler = '/objects/vote/.*'
    access = 0

    def get(self):
        if not super(ObjectVote, self).get(): return
        """ получаем голос """
        vote = str(self.request.uri.split('/')[-1])
        """ получаем ID объекта """
        objectid = int(self.request.uri.split('/')[-2])

        """ получаем id юзера """
        userid = self.Session['userid']
        
        is_nice = "unknown"
        if vote == "good":
            is_nice = True
        elif vote == "bad":
            is_nice = False
        if is_nice == "unknown":
            self.response.out.write("error")
            return
        new_vote = DBGalleryObjectRate()
        if new_vote.still_can_vote(userid, objectid):
            new_vote.vote(userid, objectid, is_nice)
        else:
            self.response.out.write("vote_exists")
            return
        self.response.out.write("vote_success")

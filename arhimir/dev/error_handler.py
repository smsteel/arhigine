from google.appengine.ext import webapp

class ErrorHandler(webapp.RequestHandler):
    """ this add / to the end of url if it`s not exist and in`s inclorrect. sry for my orcish """
    def get(self):
        uri = self.request.uri
        if uri[len(uri)-1] == '/': return
        self.redirect(uri+'/')
        
from google.appengine.ext import webapp

class RegistrationAjax(webapp.RequestHandler):
    
    def post(self):
        json = self.request.get('json')
        return if json is None
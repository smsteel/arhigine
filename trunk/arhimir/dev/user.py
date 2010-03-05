from db_entities.user import DBUser
from google.appengine.api import mail
import cgi
import re
import hashlib
import random

class User():
    
    def register(self, login, password, email, name, surname, access):
        user = DBUser()
        user.login = self.validated_login(login)
        user.password = hashlib.md5(password).hexdigest()
        user.email = self.validated_email(email)
        user.name = self.validated_name(name)
        user.surname = self.validated_surname(surname)
        confirmation = hashlib.md5(str(random.random())).hexdigest()
        user.confirmation = confirmation
        user.type = "pending"
        user.access = access
        return user.put(), confirmation

    def validated_name(self, name):
        if len(name) < 2:
            raise NameLengthSmall
        return cgi.escape(name)
    
    def validated_surname(self, surname):
        if len(surname) < 2:
            raise SurnameLengthSmall
        return cgi.escape(surname)
        
    def validated_login(self, login):
        if len(login) < 4:
            raise LoginLengthSmall
        if len(set(login) & set("~`!@#$%^&*()-=+\\/'\"{}][;:<>, ")):
            raise LoginHasRestrictedSymbols
        login = login.lower()
        if DBUser.all(keys_only=True).filter("login=", login).count(1):
            raise LoginExistsAlready
        return login
    
    def validated_email(self, email):
        if re.match("^([^@\s]+)@((?:[-a-z0-9]+\.)+[a-z]{2,})$", email) is None:
            raise EmailFormatInvalid
        email = email.lower()
        if DBUser.all(keys_only=True).filter("email=", email).count(1):
            raise EmailExistsAlready
        return email

class LoginExistsAlready(Exception):
    pass

class LoginLengthSmall(Exception):
    pass

class LoginHasRestrictedSymbols(Exception):
    pass

class EmailFormatInvalid(Exception):
    pass

class EmailExistsAlready(Exception):
    pass

class NameLengthSmall(Exception):
    pass

class SurnameLengthSmall(Exception):
    pass

print mail.is_email_valid("\ncvv bd")
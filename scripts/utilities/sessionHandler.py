from flask import session

class SessionHandler:

    def setSession(self, **kwargs):
        for key, value in kwargs.items():
            session[key] = value

    def get(self, key = None):
        if key == None:
            return session
        return session.get(key)

    def isLoggedIn(self):
        return session.get('id') is not None

    def destroySession(self):
        session.clear()

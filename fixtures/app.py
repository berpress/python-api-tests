from fixtures.auth.api import AuthUser
from fixtures.register.api import Register
from fixtures.requests import Client


class StoreApp:
    def __init__(self, url):
        self.url = url
        self.client = Client
        self.register = Register(self)
        self.auth = AuthUser(self)

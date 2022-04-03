from fixtures.auth.api import AuthUser
from fixtures.items.api import Items
from fixtures.register.api import Register
from fixtures.requests import Client
from fixtures.store.api import Store
from fixtures.user_info.api import UserInfo


class StoreApp:
    def __init__(self, url):
        self.url = url
        self.client = Client
        self.register = Register(self)
        self.auth = AuthUser(self)
        self.user_info = UserInfo(self)
        self.store = Store(self)
        self.items = Items(self)

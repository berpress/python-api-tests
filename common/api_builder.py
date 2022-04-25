from fixtures.auth.model import Auth, AuthResponse
from fixtures.register.model import RegisterUser, RegisterUserResponse
from fixtures.user_info.model import AddUserInfo


class Store:
    def __init__(self):
        self.app = None
        self.auth = Auth()
        self.header = None
        self.user_info = AddUserInfo()
        self.user_uuid = None


class ApiBuilder:
    def __init__(self, app, store: Store = None):
        if store is None:
            self.store = Store()
        else:
            self.store = store
        self.store.app = app

    def build(self) -> Store:
        return self.store

    @property
    def authentication(self):
        return AuthBuilder(self.store)

    @property
    def user_info(self):
        return UserInfoBuilder(self.store)


class AuthBuilder(ApiBuilder):
    def __init__(self, store):
        super().__init__(store.app, store)

    def register(self):
        """
        Register random user
        """
        data = RegisterUser.random()
        res = self.store.app.register.register(
            data=data, type_response=RegisterUserResponse
        )
        self.store.auth = Auth(username=data.username, password=data.password)
        self.store.user_uuid = res.data.uuid
        return self

    def auth(self):
        """
        Auth user
        """
        res = self.store.app.auth.login(
            data=self.store.auth, type_response=AuthResponse
        )
        token = res.data.access_token
        header = {"Authorization": f"JWT {token}"}
        self.store.header = header
        return self


class UserInfoBuilder(ApiBuilder):
    def __init__(self, store):
        super().__init__(store.app, store)

    def add_user_info(self):
        """
        Add user info
        """
        data = AddUserInfo.random()
        self.store.app.user_info.add_user_info(
            uuid=self.store.user_uuid, data=data, header=self.store.header
        )
        self.store.user_info = data
        return self

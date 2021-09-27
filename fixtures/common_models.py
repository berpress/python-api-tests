import attr

from fixtures.register.model import RegisterUser


@attr.s
class MessageResponse:
    message: str = attr.ib()


@attr.s
class UserStore:
    user: RegisterUser = attr.ib(default=None)
    user_uuid: int = attr.ib(default=None)

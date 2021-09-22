from faker import Faker
import attr

from fixtures.base import BaseClass

fake = Faker()


@attr.s
class RegisterUser(BaseClass):
    username: str = attr.ib(default=None)
    password: str = attr.ib(default=None)

    @staticmethod
    def random():
        return RegisterUser(username=fake.email(), password=fake.password())


@attr.s
class RegisterUserResponse:
    message: str = attr.ib()
    uuid: int = attr.ib()

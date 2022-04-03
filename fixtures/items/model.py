from faker import Faker
import attr

from fixtures.base import BaseClass

fake = Faker()


@attr.s
class Item(BaseClass):
    description: str = attr.ib(default=None)
    price: int = attr.ib(default=None)
    store_id: int = attr.ib(default=None)
    image: str = attr.ib(default=None)

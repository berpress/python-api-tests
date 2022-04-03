from fixtures.items.model import Item
from fixtures.validator import Validator
from common.deco import logging as log


class Items(Validator):
    def __init__(self, app):
        self.app = app

    POST_ADD_ITEM = "/item/{}"

    @log("Add item")
    def add_item(self, name: str, data: Item, header=None, type_response=None):
        """
        https://app.swaggerhub.com/apis-docs/berpress/flask-rest-api/1.0.0#/storeMagazine/storeAdd # noqa
        """
        response = self.app.client.request(
            method="POST",
            url=f"{self.app.url}{self.POST_ADD_ITEM.format(name)}",
            json=data.to_dict(),
            headers=header,
        )
        return self.structure(response, type_response=type_response)

from requests import Response

from fixtures.common_models import MessageResponse
from fixtures.user_info.model import AddUserInfo
from fixtures.validator import Validator
from common.deco import logging as log


class UserInfo(Validator):
    def __init__(self, app):
        self.app = app

    POST_ADD = "/user_info/{}"

    @log("Add user info")
    def add_user_info(
        self, uuid: int, data: AddUserInfo, header=None, type_response=MessageResponse
    ) -> Response:
        """
        https://app.swaggerhub.com/apis-docs/berpress/flask-rest-api/1.0.0#/userInfo/userInfoAdd # noqa
        """
        response = self.app.client.request(
            method="POST",
            url=f"{self.app.url}{self.POST_ADD.format(uuid)}",
            json=data.to_dict(),
            headers=header,
        )
        return self.structure(response, type_response=type_response)

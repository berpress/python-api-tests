from requests import Response

from fixtures.common_models import MessageResponse
from fixtures.user_info.model import AddUserInfo, GetUserInfoResponse
from fixtures.validator import Validator
from common.deco import logging as log


class UserInfo(Validator):
    def __init__(self, app):
        self.app = app

    POST_ADD_USER_INFO = "/user_info/{}"
    GET_ADD_USER_INFO = "/user_info/{}"
    DELETE_USER_INFO = "/user_info/{}"
    PUT_USER_INFO = "/user_info/{}"

    @log("Add user info")
    def add_user_info(
        self, uuid: int, data: AddUserInfo, header=None, type_response=MessageResponse
    ) -> Response:
        """
        https://app.swaggerhub.com/apis-docs/berpress/flask-rest-api/1.0.0#/userInfo/userInfoAdd # noqa
        """
        response = self.app.client.request(
            method="POST",
            url=f"{self.app.url}{self.POST_ADD_USER_INFO.format(uuid)}",
            json=data.to_dict(),
            headers=header,
        )
        return self.structure(response, type_response=type_response)

    @log("Get user info")
    def get_user_info(
        self, uuid: int, header=None, type_response=GetUserInfoResponse
    ) -> Response:
        """
        https://app.swaggerhub.com/apis-docs/berpress/flask-rest-api/1.0.0#/userInfo/userInfoGet # noqa
        """
        response = self.app.client.request(
            method="GET",
            url=f"{self.app.url}{self.POST_ADD_USER_INFO.format(uuid)}",
            headers=header,
        )
        return self.structure(response, type_response=type_response)

    @log("Delete user info")
    def delete_user_info(
        self, uuid: int, header=None, type_response=MessageResponse
    ) -> Response:
        """
        https://app.swaggerhub.com/apis-docs/berpress/flask-rest-api/1.0.0#/userInfo/userInfoDelete # noqa
        """
        response = self.app.client.request(
            method="DELETE",
            url=f"{self.app.url}{self.DELETE_USER_INFO.format(uuid)}",
            headers=header,
        )
        return self.structure(response, type_response=type_response)

    @log("Update user info")
    def update_user_info(
        self, uuid: int, data: AddUserInfo, header=None, type_response=MessageResponse
    ) -> Response:
        """
        https://app.swaggerhub.com/apis-docs/berpress/flask-rest-api/1.0.0#/userInfo/userInfoUpdate # noqa
        """
        response = self.app.client.request(
            method="PUT",
            url=f"{self.app.url}{self.PUT_USER_INFO.format(uuid)}",
            json=data.to_dict(),
            headers=header,
        )
        return self.structure(response, type_response=type_response)

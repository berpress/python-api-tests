from requests import Response

from fixtures.register.model import RegisterUser
from fixtures.validator import Validator


class Register(Validator):
    def __init__(self, app):
        self.app = app

    POST_REGISTER = "/register"

    def register(self, data: RegisterUser, type_response=None) -> Response:
        """
        https://app.swaggerhub.com/apis-docs/berpress/flask-rest-api/1.0.0#/register/regUser # noqa
        """
        response = self.app.client.request(
            method="POST",
            url=f"{self.app.url}{self.POST_REGISTER}",
            json=data.to_dict(),
        )
        return self.structure(response, type_response=type_response)

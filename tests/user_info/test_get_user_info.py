from fixtures.common_models import AuthInvalidResponse, MessageResponse
from fixtures.constants import ResponseText


class TestGetUserInfo:
    def test_get_user_info(self, app, user_info):
        """
        1. Try to get user info
        2. Check that status code is 200
        3. Check response
        """
        res = app.user_info.get_user_info(
            uuid=user_info.user_uuid, header=user_info.header
        )
        assert res.status_code == 200, "Check status code"
        assert res.data.city == user_info.user_info.address.city, "Check city"
        assert res.data.street == user_info.user_info.address.street, "Check street"
        assert res.data.email == user_info.user_info.email, "Check email"

    def test_get_user_info_wo_auth_header(self, app, user_info):
        """
        1. Try to get user info wo auth header
        2. Check that status code is 401
        3. Check response
        """
        res = app.user_info.get_user_info(
            uuid=user_info.user_uuid,
            header=None,
            type_response=AuthInvalidResponse,
        )
        assert res.status_code == 401, "Check status code"
        assert res.data.description == ResponseText.DESCRIPTION_AUTH_ERROR
        assert res.data.error == ResponseText.ERROR_AUTH_TEXT
        assert res.data.status_code == 401, "Check status code"

    def test_get_user_with_none_exist_user_id(
        self, app, user_info, none_exist_user=1000
    ):
        """
        1. Try to get user info with none exist user id
        2. Check that status code is 404
        3. Check response
        """
        res = app.user_info.get_user_info(
            uuid=none_exist_user,
            header=user_info.header,
            type_response=MessageResponse,
        )
        assert res.status_code == 404, "Check status code"
        assert res.data.message == ResponseText.MESSAGE_INFO_NOT_FOUND

from fixtures.common_models import AuthInvalidResponse, MessageResponse
from fixtures.constants import ResponseText


class TestDeleteUserInfo:
    def test_delete_user_info(self, app, user_info):
        """
        1. Try to delete user info
        2. Check that status code is 200
        3. Check response
        """
        res = app.user_info.delete_user_info(
            uuid=user_info.user_uuid, header=user_info.header
        )
        assert res.status_code == 200, "Check status code"
        assert res.data.message == ResponseText.MESSAGE_DELETE_USER_INFO

    def test_delete_user_info_wo_auth_header(self, app, user_info):
        """
        1. Try to delete user info wo auth header
        2. Check that status code is 401
        3. Check response
        """
        res = app.user_info.delete_user_info(
            uuid=user_info.user_uuid,
            header=None,
            type_response=AuthInvalidResponse,
        )
        assert res.status_code == 401, "Check status code"
        assert res.data.description == ResponseText.DESCRIPTION_AUTH_ERROR
        assert res.data.error == ResponseText.ERROR_AUTH_TEXT
        assert res.data.status_code == 401, "Check status code"

    def test_delete_user_with_none_exist_user_id(
        self, app, user_info, none_exist_user=1000
    ):
        """
        1. Try to delete user info with none exist user id
        2. Check that status code is 404
        3. Check response
        """
        res = app.user_info.delete_user_info(
            uuid=none_exist_user,
            header=user_info.header,
            type_response=MessageResponse,
        )
        assert res.status_code == 404, "Check status code"
        assert res.data.message == ResponseText.MESSAGE_INFO_NOT_FOUND_DOT

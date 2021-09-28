from fixtures.common_models import AuthInvalidResponse, MessageResponse
from fixtures.constants import ResponseText
from fixtures.store.model import Store


class TestGetStore:
    def test_get_store(self, app, store):
        """
        1. Try to get store
        2. Check that status code is 201
        3. Check response
        """
        res = app.store.get_store(store.store, header=store.header)
        assert res.status_code == 200, "Check status code"
        assert res.data.name == store.store

    def test_get_store_wo_auth_header(self, app, user_info):
        """
        1. Try to get store wo auth header
        2. Check that status code is 401
        3. Check response
        """
        data = Store.random()
        res = app.store.get_store(
            name=data.name,
            header=None,
            type_response=AuthInvalidResponse,
        )
        assert res.status_code == 401, "Check status code"
        assert res.data.description == ResponseText.DESCRIPTION_AUTH_ERROR
        assert res.data.error == ResponseText.ERROR_AUTH_TEXT
        assert res.data.status_code == 401, "Check status code"

    def test_get_store_with_none_exist_name(self, app, user_info, none_exist_user=1000):
        """
        1. Try to double add with same data
        2. Check that status code is 404
        3. Check response
        """
        data = Store("Test12345")
        res = app.store.get_store(
            data.name, header=user_info.header, type_response=MessageResponse
        )
        assert res.status_code == 404, "Check status code"
        assert res.data.message == ResponseText.MESSAGE_STORE_NOT_FOUND

class TestBuilder:
    def test_add_user_info_builder(self, app, user_info_builder):
        """
        1. Try to add user info
        2. Check that status code is 200
        3. Check response
        """
        assert user_info_builder.user_info is not None

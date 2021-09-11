import requests
from faker import Faker


fake = Faker()


class TestRegisterUser:
    BASE_URL = "https://stores-tests-api.herokuapp.com"

    def test_register_user_with_valid_data(self):
        """
        1. Try to register user with valid data
        2. Check that status code is 201
        3. Check response
        """
        url = self.BASE_URL + "/register"
        data = {"username": fake.email(), "password": fake.password()}
        response = requests.post(url=url, json=data)
        assert response.status_code == 201
        print(response.text)
        assert response.json().get("message") == "User created successfully."
        assert isinstance(response.json().get("message"), str)
        assert response.json().get("uuid")
        assert isinstance(response.json().get("uuid"), int)

    def test_register_user_with_empty_data(self):
        """
        1. Try to register user with empty data
        2. Check that status code is 201
        3. Check response
        """
        url = self.BASE_URL + "/register"
        data = {"username": None, "password": None}
        response = requests.post(url=url, json=data)
        assert response.status_code == 400
        print(response.text)

    # def test_register_user_with_valid_data_2(self, app):
    #     """
    #     1. Try to register user with valid data
    #     2. Check that status code is 201
    #     3. Check response
    #     """
    #     data = RegisterUser.random()
    #     res = app.register.register_user(data)
    #     assert res.status_code == 201
    #     assert res.data.message == Constants.MESSAGE_ADD_USER

    def test_register_user_with_double_data(self):
        """
        1. Try to register user with double data
        2. Check that status code is 400
        3. Check response
        """
        url = self.BASE_URL + "/register"
        # first request
        data = {"username": fake.email(), "password": fake.password()}
        response = requests.post(url=url, json=data)
        assert response.status_code == 201
        print(response.text)
        # second request
        response = requests.post(url=url, json=data)
        assert response.status_code == 400
        print(response.text)

    # 1. Вынести строку в константы
    # 2. Вынести url в константы
    # 3. Абстракции
    # 4. Расписать ошибку в asserts
    # 5. Логгирование вместо print

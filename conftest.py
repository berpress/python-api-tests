import logging

import pytest
from swagger_coverage.src.coverage import SwaggerCoverage

from common.api_builder import ApiBuilder

from fixtures.app import StoreApp
from fixtures.common_models import UserStore
from fixtures.register.model import RegisterUser
from fixtures.store.model import Store
from fixtures.user_info.model import AddUserInfo

logger = logging.getLogger("api")


@pytest.fixture(scope="session")
def app(request):
    url = request.config.getoption("--api-url")
    logger.info(f"Start api tests, url is {url}")
    return StoreApp(url)


@pytest.fixture
def register_user(app) -> UserStore:
    """
    Register new user
    """
    data = RegisterUser.random()
    res = app.register.register(data=data)
    data = UserStore(user=data, user_uuid=res.data.uuid)
    return data


@pytest.fixture
def auth_user(app, register_user) -> UserStore:
    """
    Login user
    """
    res = app.auth.login(data=register_user.user)
    token = res.data.access_token
    header = {"Authorization": f"JWT {token}"}
    data = UserStore(**register_user.to_dict())
    data.header = header
    return data


@pytest.fixture
def user_info(app, auth_user) -> UserStore:
    """
    Add user info
    """
    data = AddUserInfo.random()
    app.user_info.add_user_info(
        uuid=auth_user.user_uuid, data=data, header=auth_user.header
    )
    data_user = UserStore(**auth_user.to_dict())
    data_user.user_info = data
    return data_user


@pytest.fixture
def store(app, user_info) -> UserStore:
    """
    Add store
    """
    data = Store.random()
    app.store.add_store(data.name, header=user_info.header)
    data_store = UserStore(**user_info.to_dict())
    data_store.store = data.name
    return data_store


def pytest_addoption(parser):
    parser.addoption(
        "--api-url",
        action="store",
        help="enter api url",
        default="https://stores-tests-api.herokuapp.com",
    ),
    parser.addoption(
        "--swagger-url",
        action="store",
        help="enter swagger url",
        default="https://api.swaggerhub.com/apis/berpress/flask-rest-api/1.0.0",
    ),


@pytest.fixture(scope="session", autouse=True)
def swagger_checker(request):
    url = request.config.getoption("--swagger-url")
    url_api = request.config.getoption("--api-url")
    path = "/report"
    swagger = SwaggerCoverage(api_url=url_api, url=url, path=path)
    swagger.create_coverage_data()
    yield
    swagger.create_report()


@pytest.fixture
def user_info_builder(app):
    app_builder = ApiBuilder(app)
    user = (
        app_builder.authentication.register().auth().user_info.add_user_info().build()
    )
    return user

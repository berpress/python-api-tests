import logging

import pytest

from fixtures.app import StoreApp
from fixtures.common_models import UserStore
from fixtures.register.model import RegisterUser

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


def pytest_addoption(parser):
    parser.addoption(
        "--api-url",
        action="store",
        help="enter api url",
        default="https://stores-tests-api.herokuapp.com",
    ),

import pytest
from pytest_bdd import scenario, given, when, then


@scenario(
    "./features/login/init.feature",
    "Can be initialized with username and password",
)
def test_init_with_username_and_password():
    pass


@given("that luucy-python is installed")
def luucy_installed():
    from luucy import LUUCY


@pytest.fixture()
@when("a username and password are set")
def load_config():
    return {"username": "luucy", "password": "lucerneCity"}


@then("it loads successfully")
def luucy_loaded(load_config):
    from luucy import LUUCY

    LUUCY(username=load_config["username"], password=load_config["password"])

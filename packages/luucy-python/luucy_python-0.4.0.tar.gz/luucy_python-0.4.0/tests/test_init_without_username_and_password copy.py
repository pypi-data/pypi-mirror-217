import pytest
from pytest_bdd import scenario, given, when, then


@scenario(
    "./features/login/init.feature",
    "Raises an exception if no username and password are supplied",
)
def test_init_without_username_and_password():
    pass


@given("that luucy-python is installed")
def luucy_installed():
    from luucy import LUUCY


@pytest.fixture()
@when("no username and password are set")
def load_config():
    pass


@then("it raises and exception")
def luucy_loaded(load_config):
    from luucy import LUUCY

    with pytest.raises(ValueError) as e_info:
        LUUCY()

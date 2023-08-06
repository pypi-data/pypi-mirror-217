from pytest_bdd import scenario, given, when, then
from luucy import LUUCY
import os


@scenario("./features/login/init.feature", "Can be used with production environment")
def test_switching_environments():
    pass


@given("the baseUrl is set not set")
@when("initiating the client")
@then("production is used")
def test_staging(mock_login_request):
    LUUCY(username="luucy", password="lucerneCity")

    assert os.environ["REQUEST_URL"] == "https://app.luucy.ch/api/login"

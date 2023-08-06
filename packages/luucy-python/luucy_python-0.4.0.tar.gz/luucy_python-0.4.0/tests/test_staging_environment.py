from pytest_bdd import scenario, given, when, then
from luucy import LUUCY
import os


@scenario("./features/login/init.feature", "Can be used with different environments")
def test_switching_environments():
    pass


@given("the baseUrl is set to staging")
@when("initiating the client")
@then("staging is used")
def test_staging(mock_login_request):
    client = LUUCY(
        username="luucy", password="lucerneCity", base_url="app.staging.luucy.ch"
    )

    assert os.environ["REQUEST_URL"] == "https://app.staging.luucy.ch/api/login"

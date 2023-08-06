from pytest_bdd import scenario, given, when, then
from luucy import LUUCY


@scenario("./features/login/init.feature", "Returns user data")
def test_login_returns_user_data():
    pass


@given("the client is logged in")
@when("user_data is called")
@then("user data of logged in user is returned")
def account_info(mock_login_request):
    client = LUUCY(username="luucy", password="lucerneCity")

    assert client.user_id == 1234
    assert client.api_token is not None

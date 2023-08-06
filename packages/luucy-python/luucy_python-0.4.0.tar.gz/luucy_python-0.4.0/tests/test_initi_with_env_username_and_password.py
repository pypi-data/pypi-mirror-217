from pytest_bdd import scenario, given, when, then


@scenario(
    "./features/login/init.feature",
    "Can be initialized with environment username and password",
)
def test_init_with_env_username_and_password():
    pass


@given("that luucy-python is installed")
def luucy_installed():
    from luucy import LUUCY


@when(
    "a usernamane and password are set via LUUCY_USERNAME and LUUCY_PASSWORD environment variables",
)
def load_config(monkeypatch):
    monkeypatch.setenv("LUUCY_USERNAME", "luucy")
    monkeypatch.setenv("LUUCY_PASSWORD", "lucerneCity")


@then("it loads successfully")
def luucy_loaded():
    from luucy import LUUCY

    LUUCY()

from typing import Optional
import os
import json
import requests


class LUUCY:
    """A high level object to initiate a client.

    Parameters:
        username: LUUCY username.
        password: LUCUY password.

    Raises:
        ValueError: When no `username` and `password` are supplied
    """

    def __init__(
        self,
        username: Optional[str] = None,
        password: Optional[str] = None,
        base_url: str = "app.luucy.ch",
    ):
        self._username = username
        self._password = password
        self._base_url = base_url
        self._user_id = None

        if os.environ.get("LUUCY_USERNAME", None) and os.environ.get(
            "LUUCY_PASSWORD", None
        ):
            self._username = os.environ["LUUCY_USERNAME"]
            self._password = os.environ["LUUCY_PASSWORD"]

        if self._username and self._password:
            account = requests.post(
                url=f"https://{self._base_url}/api/login",
                headers={
                    "Content-Type": "application/json; charset=utf-8",
                },
                data=json.dumps(
                    {
                        "login": self._username,
                        "password": self._password,
                        "rememberMe": True,
                    }
                ),
                timeout=300,
            )
            if account.status_code == 200:
                self._user_id = account.json()["person"]["id"]
                self._api_token = account.json()["apiKey"]

            return None

        raise ValueError("username or password is empty")

    @property
    def user_id(self) -> Optional[int]:
        return self._user_id

    @property
    def api_token(self) -> Optional[str]:
        return self._api_token

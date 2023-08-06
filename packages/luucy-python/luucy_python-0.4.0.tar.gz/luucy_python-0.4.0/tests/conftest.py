import pytest
import requests


class MockResponse:
    def __init__(self, json_data, status_code):
        self.json_data = json_data
        self.status_code = status_code

    def json(self):
        return self.json_data


@pytest.fixture
def mock_login_request(monkeypatch):
    def mock_login_request_func(url, *args, **kwargs):
        monkeypatch.setenv("REQUEST_URL", url)

        return MockResponse(
            {
                "apiKey": "18b8c9a1234599b5043e654321e0c870956aga09",
                "person": {
                    "id": 1234,
                    "name": "Luucy",
                    "surname": "Tester",
                    "lastLoginDate": "2023-07-04T19:41:43.746368+02:00",
                    "email": "luucy@luucy.ch",
                    "language": "EN",
                    "design": None,
                    "sendNotifications": True,
                    "isConfirmed": True,
                    "isOrgAdmin": False,
                    "confirmUntil": None,
                    "defaultWorkspaceId": None,
                    "userSettings": [
                        {"userId": 1234, "key": "activeOrgId", "value": "1"},
                        {
                            "userId": 1234,
                            "key": "agreementTime",
                            "value": "2023-02-01T10:20:14.501171Z",
                        },
                        {"userId": 1234, "key": "cameraOverTerrain", "value": "false"},
                        {"userId": 1234, "key": "depthOfFocus", "value": "false"},
                        {"userId": 1234, "key": "displayDepth", "value": "32"},
                        {"userId": 1234, "key": "displayQuality", "value": "NORMAL"},
                        {"userId": 1234, "key": "edgeDrawing", "value": "false"},
                        {"userId": 1234, "key": "news", "value": "true"},
                        {"userId": 1234, "key": "occlusion", "value": "true"},
                        {
                            "userId": 1234,
                            "key": "showInterventionHelp",
                            "value": "false",
                        },
                        {"userId": 1234, "key": "terms", "value": "true"},
                        {"userId": 1234, "key": "tourGuide", "value": "true"},
                    ],
                },
            },
            200,
        )

    monkeypatch.setattr(requests, "post", mock_login_request_func)

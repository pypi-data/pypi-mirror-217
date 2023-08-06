class LUUCY:
    def __init__(self, username=None, password=None):
        self._username = username
        self._password = password

        if not self._username or not self._password:
            raise ValueError("username or password is empty")

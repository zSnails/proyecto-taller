from models import Account
from getpass import getpass
from secrets import token_hex
from hashlib import sha256
from json import load, dump, JSONDecodeError
# NOTE: use a database such as mysql or mongo to store data
class Auth:
    """Authentication helper class for internal authentication"""
    __instance = None

    def __new__(cls):
        if Auth.__instance is None:
            Auth.__instance = object.__new__(cls)

        return Auth.__instance

    def __init__(self):
        self.auth_data = {}

    def load_data(self):
        """Helper function to load data"""

        with open("auth.json", "r", encoding="utf-8") as f:
            self.auth_data = load(f)

    def check_existence(self, username: str) -> bool:
        if not self.auth_data.get(username): return False
        return True

    def store_password(self, username: str, password: str) -> bool:
        """Helper function to store passwords in the password 'database'"""
        # add salt to the password
        salt = token_hex(8)

        hashed_pass = sha256(f'{salt}{password}'.encode()).hexdigest()

        if not self.auth_data.get(username):
            self.auth_data[username] = f"{salt}:{hashed_pass}"
        else: return False
        with open("auth.json", "w", encoding="utf-8") as auth_file:
            dump(self.auth_data, auth_file)
        self.load_data()

        return True

    def verify_account(self, name: str, password: str) -> bool:
        """Helper function to verify valid login data"""

        self.load_data()

        data = self.auth_data.get(name)
        if not data:
            return False
        salt, _password = data.split(':')
        hashed_pass = sha256(f"{salt}{password}".encode()).hexdigest()
        return _password == hashed_pass

# a = Auth()

# a.store_password('zsnails', 'sex')
# a.verify_account('zsnails', 'sex')

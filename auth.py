from pickle import dump, load
from classes import Account
from getpass import getpass
from manager import Manager

# TODO: use a database such as mysql or mongo to store data
class Auth:
    """Authentication helper class for internal authentication"""
    __instance = None

    def __new__(cls):
        if Auth.__instance is None:
            Auth.__instance = object.__new__(cls)

        return Auth.__instance

    def __init__(self):
        self.auth_data = {}
        self.load_data()

    def load_data(self):
        """Helper function to load data"""
        with open("auth.pkl", "rb") as f:
            self.auth_data = load(f)

    # NOTE: this isn't a good practice, but it gets the job done here, so I will be
    # using this until I decide to change it to an actual password store
    # TODO: use a better authentication system
    def store_password(self, username: str, password: str) -> None:
        """Helper function to store passwords in the password 'database'"""

        self.auth_data[username] = password
        with open("auth.pkl", "wb") as auth_file:
            dump(auth_data, auth_file)
        self.load_data()

    def verify_account(self, name: str, password: str) -> bool:
        """Helper function to verify valid login data"""
        return self.auth_data.get(name) == password

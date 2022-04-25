from models import Account
from secrets import token_hex
from hashlib import sha256
from json import load, dump, JSONDecodeError
# NOTE: use a database such as mysql or mongo to store data
class Auth:
    """
    The Auth class manages all authentication related jobs

    Parameters
    ----------
        -   None
    """
    __instance = None

    def __new__(cls):
        """
        This __new__ method is being used to instantiate a singleton
        the main idea behind this was that I'd be using the class in multiple places
        although at the end I ended up not using the singleton feature of this class
        """
        if Auth.__instance is None:
            Auth.__instance = object.__new__(cls)

        return Auth.__instance

    def __init__(self):
        """
        The __init__ special method is responsible for class initialization
        here we set the instance property `auth_data`
        """
        self.auth_data = {}

    def load_data(self):
        """
        The load data function loads auth data to memory, the loaded data is stored
        in the `auth_data` property
        """

        with open("auth.json", "r", encoding="utf-8") as f:
            self.auth_data = load(f)


    def check_existence(self, username: str) -> bool:
        """
        This method checks whether or not the user exsists in the
        auth database
        
        Parameters
        ----------
            username: The username to look for
        
        Returns
        -------
            - bool: Whether or not the user exists
        """
        if not self.auth_data.get(username): return False
        return True

    
    def store_password(self, username: str, password: str) -> bool:
        """
        The store password method saves an username and password into the passwords
        `database`

        Parameters
        ----------
            -   username: The username to be stored
            -   password: The password to be stored

        Returns
        -------
            -   bool: whether or not the password was saved
        """
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
        """
        The verify_account method checks whether or not the username and password
        provided by the user are stored in the database, and whether or not the credentials
        are correct, it used a sha256 hash function and a `salt` to mangle the password so that
        known passwords cannot be cracked easily if there's ever a database leak

        Parameters
        ----------
            -   name: The account's name
            -   password: The account's password

        Returns
        -------
            -   bool: whether or not the credentials pair was correct
        """

        self.load_data()

        data = self.auth_data.get(name)
        if not data:
            return False
        salt, _password = data.split(':')
        hashed_pass = sha256(f"{salt}{password}".encode()).hexdigest()
        return _password == hashed_pass

from pickle import dump, load

auth_data = {}

with open("auth.pkl", "rb") as f:
    auth_data = load(f)

def store_password(username: str, password: str) -> None:
    """Helper function to store passwords in the password 'database'"""

    auth_data[username] = password

    with open("auth.pkl", "wb") as auth_file:
        dump(auth_data, auth_file)
        auth_file.close()
    with open("auth.pkl", "rb") as auth_file:
        auth_data = load(auth_file)

def verify_account(name: str, password: str) -> bool:
    """Helper function to verify valid login data"""

    if auth_data[name] == password:
        return True
    return False


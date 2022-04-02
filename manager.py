from classes import Career, Course, Account, AccountType
from typing import List, Dict
from pickle import dump, load


class Manager:

    courses: List[Course]
    accounts: List[Account]
    careers: List[Career]

    def get_courses() -> List[Course]:
        pass

    def get_accounts() -> List[Account]:
        pass

    def get_students() -> List[Account]:
        pass

    def get_admins() -> List[Account]:
        pass
    
    def get_careers() -> List[Career]:
        pass

def load_data(file_name: str) -> Dict:
    pass

def get_manager() -> Manager:
    mngr = Manager()


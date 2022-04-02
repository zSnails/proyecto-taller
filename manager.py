from classes import Career, Course, Account, AccountType
from typing import List, Dict
from json import load, dump


class Manager:

    # courses: List[Course]
    # accounts: List[Account]
    # careers: List[Career]

    def __init__(self):
        self.courses: List[Course] = []
        self.accounts: List[Account] = []
        self.careers: List[Career] = []

    def get_courses(self) -> List[Course]:
        pass

    def get_accounts(self) -> List[Account]:
        pass

    def get_students(self) -> List[Account]:
        pass

    def get_admins(self) -> List[Account]:
        pass
    
    def get_careers(self) -> List[Career]:
        pass

def get_manager() -> Manager:
    """Helper function to initialize and fill a manager instance"""

    mngr = Manager()
    with open('data.json', 'r') as f:
        data = load(f)
        print(data)
        for account in data["accounts"]:
            mngr.accounts.append(Account(**account))

        for course in data["courses"]:
            mngr.courses.append(Course(**course))

        for career in data["careers"]:
            mngr.careers.append(Career(**career))
        
    return mngr

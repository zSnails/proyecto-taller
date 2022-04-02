from classes import Career, Course, Account, AccountType
from typing import List, Dict, Optional
from json import load, dump


class Manager:
    """
    Manager class to manage internal data

    Arguments
    ---------
        None
    Returns
    -------
        None
    """

    def __init__(self):
        self.courses: List[Course] = []
        self.accounts: List[Account] = []
        self.careers: List[Career] = []

        # Current user used for auth
        self.current_user: Account


    def set_current(self, user: Account) -> None:
        self.current_user = user

    def get_courses(self) -> List[Course]:
        """
        Returns a list containing all registered courses

        Parameters
        ----------
            None

        Returns
        -------
         - A list containing all registered courses
        """
        return self.courses

    def get_accounts(self) -> List[Account]:
        """
        Returns a list containing all registered accounts, including students
        and admin accounts

        Parameters
        ----------
            None

        Returns
        -------
         - A list containing all registered accounts
        """
        return self.accounts

    def get_students(self) -> List[Account]:
        """
        Returns a list containing all registered student accounts

        Parameters
        ----------
            None

        Returns
        -------
         - A list containing all accounts with an account type of STUDENT
        """
        return [student for student in self.accounts if student._type == AccountType.STUDENT]
    
    def get_student(self,
            name: str = None,
            id: int = None) -> Optional[Account, None]:
        """
        Returns a user whose name or id are equal to either argument

        Parameters
        ----------
         - name: a valid username
         - id: a valid user id

        Returns
        -------
         - A student or None
        """
        for student in self.get_students():
            if student.name == name or student.id == id:
                return student
        return None

    def get_admins(self) -> List[Account]:
        """
        Returns a list containing all registered admin accounts

        Parameters
        ----------
            None

        Returns
        -------
         - A list containing all accounts with an account type of ADMIN
        """
        return [admin for admin in self.accounts if admin._type == AccountType.ADMIN]

    def get_admin(self,
            username: str = None,
            id: int = None) -> Optional[Account, None]:
        """
        Returns a user whose name or id are equal to either argument

        Parameters
        ----------
         - name: a valid username
         - id: a valid user id

        Returns
        -------
         - An admin or None
        """
        for admin in self.get_admins():
            if admin.name == username or admin.id == id:
                return admin

        return None

    def get_careers(self) -> List[Career]:
        """
        Returns a list containing all registered careers

        Parameters
        ----------
            None

        Returns
        -------
         - A list containing all registered careers
        """
        return self.careers
    def get_career(self, name: str = None, id: int = None):
        for career in self.careers:
            if career.name == name or career.id == id:
                return career

        return None

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

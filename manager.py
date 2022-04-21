from models import Career, Course, Account, AccountRole
from typing import List, Dict, Optional, Literal
from json import load, dump


class Manager:
    """
    Manager class to manage internal data
    """

    __instance = None

    def __new__(cls):
        if Manager.__instance is None:
            Manager.__instance = object.__new__(cls)

        return Manager.__instance

    def __init__(self):
        self.courses: List[Course] = []
        self.accounts: List[Account] = []
        self.careers: List[Career] = []
        self._load_db()

    def _load_db(self):
        with open('data.json', 'r', encoding="utf-8") as f:
            data = load(f)
            for account in data["accounts"]:
                self.accounts.append(Account(**account))

            for course in data["courses"]:
                self.courses.append(Course(**course))

            for career in data["careers"]:
                self.careers.append(Career(**career))

    def get_account(self, name: str = None,
            id: int = None) -> Optional[Account]:
        """
        Returns an account that matches the specified data

        Parameters
        ----------
         - name: The name of a valid account
         - id: The id of a valid account
        """

        for account in self.accounts:
            if account.name == name or account.id == id:
                return account
        return None

    def get_courses(self, career_id: int) -> List[Course]:
        """
        Returns a list containing all registered courses for the passed career

        Parameters
        ----------
         - career: A valid career id

        Returns
        -------
         - A list containing all registered courses available for the passed career
        """
        return [course for course in self.courses if career_id in course.belongs_to]

    def get_accounts(self) -> List[Account]:
        """
        Returns a list containing all registered accounts, including students
        and admin accounts

        Parameters
        ----------
         - None

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
         - None

        Returns
        -------
         - A list containing all accounts with an account type of STUDENT
        """
        return [student for student in self.accounts if student._type == AccountRole.STUDENT]

    def get_student(self,
            name: str = None,
            id: int = None) -> Optional[Account]:
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
         - None

        Returns
        -------
         - A list containing all accounts with an account type of ADMIN
        """
        return [admin for admin in self.accounts if admin._type == AccountRole.ADMIN]

    def get_admin(self,
            username: str = None,
            id: int = None) -> Optional[Account]:
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
         - None

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

    def register_career(self, career: Career):
        with open("data.json", "r", encoding="utf-8") as f:
            data = load(f)
            data["careers"].append(career.dict())

        with open("data.json", "w", encoding="utf-8") as f:
            dump(data, f)

        self._load_db()

    def register_user(self, user: Account, password: str = None) -> Optional[bool]:
        """
        Registers a new user to the 'data' database

        Parameters
        ----------
         - user: The user to be registered
         - password: the user's password

        Returns
        -------
         - bool: Wether or not the user was registered
        """
        with open("data.json", "r", encoding="utf-8") as f:
            data = load(f)
            data["accounts"].append(user.dict())

        with open("data.json", "w", encoding="utf-8") as f:
            dump(data, f)

        # update cache
        # TODO: find a better workaround
        self._load_db()

    def register_course(self, course: Course):
        with open("data.json", "r", encoding="utf-8") as f:
            data = load(f)
            data["courses"].append(course.dict())

        with open("data.json", "w", encoding="utf-8") as f:
            dump(data, f, default=str)

        self._load_db()

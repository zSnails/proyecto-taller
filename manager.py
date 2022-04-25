from models import Career, Course, Account, AccountRole, Activity
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
        self.activities: List[Activity] = []
        self._load_db()

    def _load_db(self):
        """
        The _load_db function updates the current state of the programs data
        it also resets all the data to update it
        
        Returns
        -------
            -    None
        """
        self.accounts = []
        self.courses = []
        self.careers = []
        self.activities = []
        with open('data.json', 'r', encoding="utf-8") as f:
            data = load(f)
            for account in data["accounts"]:
                self.accounts.append(Account(**account))

            for course in data["courses"]:
                self.courses.append(Course(**course))

            for career in data["careers"]:
                self.careers.append(Career(**career))

            for activity in data["activities"]:
                self.activities.append(Activity(**activity))

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

    def get_activities(self):
        return self.activities

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

    def get_career(self, name: str = None, id: int = None) -> Career:
        """
        The get career method returns a career based on either its id or name

        Both parameters are optional, but at least one must be provided

        Parameters
        ----------
            -   name: The name of the career
            -   id: the id of the career

        Returns
        -------
            -   Career: a career instance containing the requested data
        """
        for career in self.careers:
            if career.name == name or career.id == id:
                return career

    def get_account_courses(self, id=None, name=None) -> List[Course]:
        """
        This method returns a list containig all registered courses on requested user

        Both parameters are optional, but at least one must be provided

        Parameters
        ----------
            -   id: The id of the user
            -   name: The name of the user

        Returns
        -------
            -   List[Course]: A list containing all valid courses for the requested user
        """

        usr = self.get_account(id=id, name=name)
        if usr:
            return [course for course in self.courses if course.id in usr.courses]

    def register_career(self, career: Career):
        """
        This mehod registers a new career and saves it to the careers db

        Parameters
        ----------
            -   career: A career instance to be stored in the database

        Returns
            -   None
        """
        with open("data.json", "r", encoding="utf-8") as f:
            data = load(f)
            data["careers"].append(career.dict())

        with open("data.json", "w", encoding="utf-8") as f:
            dump(data, f)

        self._load_db()

    def register_user(self, user: Account) -> Optional[bool]:
        """
        Registers a new user to the 'data' database

        Parameters
        ----------
         - user: The user to be registered

        Returns
        -------
         - bool: Wether or not the user was registered
        """

        with open("data.json", "r", encoding="utf-8") as f:
            data = load(f)
            data["accounts"].append(user.dict())

        with open("data.json", "w", encoding="utf-8") as f:
            dump(data, f)

        self._load_db()

    def update_account_courses(self, course: Course, account_id=None, account_name=None):
        """
        This method updates the registered courses on a specific account
        it's used to add courses, but not remove them

        Parameters
        ----------
            -   course: The couse to be added
            -   account_id: The id if the account to update
            -   account_name: The name of the account to update

        Returns
        -------
            -   None
        """
        with open("data.json", "r", encoding="utf-8") as f:
            data = load(f)
            for account in data["accounts"]:
                if account["id"] == account_id or account["name"] == account_name:
                    account["courses"].append(course)
        with open("data.json", "w", encoding="utf-8") as f:
            dump(data, f, default=str)

        self._load_db()

    def update_user_course_status(self, status: str, course_id=None,
            account_id=None, account_name=None):
        """
        This method updated the current status of a specific course on a specific user
        this is used to change the status to passed or failed

        Parameters
        ----------
            -   status: The status, if it's passed or failed
            -   course_id: The id of the course to be updated
            -   account_id: The id of the account to be updated
            -   account_name: The name of the account to be updated

        Returns
        -------
            -   None
        """
        with open("data.json", "r", encoding="utf-8") as f:
            data = load(f)
            for account in data["accounts"]:
                if account["id"] == account_id or account["name"] == account_name:
                    account[status].append(int(course_id))
        with open("data.json", "w", encoding="utf-8") as f:
            dump(data, f)

        self._load_db()

    def register_course(self, course: Course):
        """
        This method registers a new course and saves it to the `database`
        
        Parameters
        ----------
            -   course: A course instance to be saved to the `database`

        Returns
        -------
            -   None
        """
        with open("data.json", "r", encoding="utf-8") as f:
            data = load(f)
            data["courses"].append(course.dict())

        with open("data.json", "w", encoding="utf-8") as f:
            dump(data, f, default=str)

        self._load_db()

    def register_activity(self, activity: Activity):
        """
        This method registers an activity and saves it to the database

        Parameters
        ----------
            -   activity: An activity instance to be saved to the database

        Returns
            -   None
        """
        with open("data.json", "r", encoding="utf-8") as f:
            data = load(f)
            data["activities"].append(activity.dict())
        with open("data.json", "w", encoding="utf-8") as f:
            dump(data, f, default=str)

        self._load_db()

    def update_activity(self, id=None):
        """
        This method updates a specific activity and marks it as done, this cannot be reverted

        Parameters
        ----------
            -   id: The id of the activity to update

        Returns
        -------
            -   None
        """
        with open("data.json", "r", encoding="utf-8") as f:
            data = load(f)
            for activity in data["activities"]:
                if activity["id"] == id:
                    activity["done"] = True
        with open("data.json", "w", encoding="utf-8") as f:
            dump(data, f)

        self._load_db()

    def switch_account_career(self, career_id=None, account_id=None):
        """
        This method updated a specific account and switches its career

        Parameters
        ----------
            -   career_id: The id of the career to update
            -   account_id: The id of the account to update

        Returns
        -------
            -   None
        """

        with open("data.json", "r", encoding="utf-8") as f:
            data = load(f)
            for acc in data["accounts"]:
                if acc["id"] == account_id:
                    acc["career"] = career_id
        with open("data.json", "w", encoding="utf-8") as f:
            dump(data, f)

        self._load_db()
    
    def add_activity_to_user(activity_id, user_id):
        """
        This method updates a specified user's activities and appends a
        new activity to them
        
        Parameters
        ----------
            -    activity_id: The id of the activity to add to the user
            -    user_id: The id of the user to be updated
        """

        with open("data.json", "r", encoding="utf-8") as f:
            data = load(f)
            for user in data["users"]:
                if user["id"] == user_id:
                    user["activities"].append(activity_id)
        with open("data.json", "w", encoding="utf-8") as f:
            dump(data, f)

        self._load_db()
    
    def reset_account_courses(self, account_id=None):
        """
        This method resets the specified user's courses list
        this is to be used when switching career
        
        Parameters
        ----------
            -    account_id: The id of the ueser to be updated
        
        Returns
        -------
            -    None
        """

        with open("data.json", "r", encoding="utf-8") as f:
            data = load(f)
            for acc in data["accounts"]:
                if acc["id"] == account_id:
                    acc["courses"] = []
                    acc["passed"] = []
                    acc["failed"] = []
        with open("data.json", "w", encoding="utf-8") as f:
            dump(data, f)

        self._load_db()
        
    def switch_account_report_type(self, account_id=None):
        """
        The `switch_account_report_type` method updates an account's report typa
        
        Parameters
        ----------
            -    account_id: The id of the account to look for
        
        Returns
        -------
            -    None
        """

        with open("data.json", "r", encoding="utf-8") as f:
            data = load(f)

            for acc in data["accounts"]:
                if acc["id"] == account_id:
                    r = acc["reports"]
                    if r == 1:
                        acc["reports"] = 2
                    elif r == 2:
                        acc["reports"] = 1

        with open("data.json", "w", encoding="utf-8") as f:
            dump(data, f)
        self._load_db()

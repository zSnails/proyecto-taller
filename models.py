from pydantic import BaseModel, ValidationError
from enum import IntEnum, auto
from datetime import date, time
from typing import List, Tuple, Optional

class Career(BaseModel):
    """
    The career model holds information related to a specific career
    such as its id and name
    """

    id: int
    name: str

class WeekDays(IntEnum):
    """
    The weekdays enum represents each day of the week with MONDAY being = 1 and SUNDAY = 7
    """

    MONDAY      = auto()
    TUESDAY     = auto()
    WEDNESDAY   = auto()
    THURSDAY    = auto()
    FRIDAY      = auto()
    SATURDAY    = auto()
    SUNDAY      = auto()

class ReportType(IntEnum):
    """
    The reporttype enum is used to represent an user's report type (daily or weekly)
    """

    DAILY   = auto()
    WEEKLY  = auto()

class Course(BaseModel):
    """
    The course model represents and holds information about a course
    such as its id, name and credits
    """

    id: int
    name: str
    credits: int
    course_hours: int
    weekly_hours: int
    start_date: date
    end_date: date
    schedule: List[Tuple[int, time, time]]
    belongs_to: List[int]


class AccountRole(IntEnum):
    """
    The accountrole enum represents the different account type the program has
    with STUDENT = 1 and ADMIN = 2
    """

    STUDENT = auto()
    ADMIN   = auto()


class Account(BaseModel):
    """
    The account model represents and holds information about an account
    it holds the different properties that an account might have
    such as the name and courses
    """

    id: int
    name: str
    courses: List[int] = []
    passed: List[int] = []
    failed: List[int] = []
    activities: List[int] = []
    career: int
    role: AccountRole
    reports: ReportType
    phone_number: str


class Activity(BaseModel):
    """
    The activity model represents and holds information about an activity
    it holds all of its properties, ranging from the id of the activity to the end_hour of said activity
    """

    id: int
    name: str
    belongs_to: int
    description: str
    course: Optional[int] = None
    activity_date: date
    done: bool
    start_hour: time
    end_hour: time


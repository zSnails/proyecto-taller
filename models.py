from pydantic import BaseModel, ValidationError
from enum import IntEnum, auto
from datetime import date, time
from typing import List, Tuple, Optional


class LinkedList:
    def __init__(self):
        self.head = None
        self.length = 0

    def __len__(self):
        return self.length

    def append(self, data) -> None:
        if not self.head:
            self.head = data
            self.length += 1
            return

        current = self.head
        while current.next:
            current = current.next
        current.next = data
        self.length += 1

    def __iter__(self) -> "Node":
        curr = self.head
        while curr:
            yield curr
            curr = curr.next


class Career(BaseModel):
    """
    The career model holds information related to a specific career
    such as its id and name
    """

    id: int
    name: str
    next: Optional["Career"] = None


Career.update_forward_refs()


class WeekDays(IntEnum):
    """
    The weekdays enum represents each day of the week with MONDAY being = 1 and SUNDAY = 7
    """

    MONDAY = auto()
    TUESDAY = auto()
    WEDNESDAY = auto()
    THURSDAY = auto()
    FRIDAY = auto()
    SATURDAY = auto()
    SUNDAY = auto()


class ReportType(IntEnum):
    """
    The reporttype enum is used to represent an user's report type (daily or weekly)
    """

    DAILY = auto()
    WEEKLY = auto()


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
    next: Optional["Course"] = None


# Needed to prevent field 'x' not yet prepared so type is still a forward ref
Course.update_forward_refs()


class AccountRole(IntEnum):
    """
    The accountrole enum represents the different account type the program has
    with STUDENT = 1 and ADMIN = 2
    """

    STUDENT = auto()
    ADMIN = auto()


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
    phone_number: Optional[str] = ""
    next: Optional["Account"] = None


# Needed to prevent field 'x' not yet prepared so type is still a forward ref
Account.update_forward_refs()


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
    next: Optional["Activity"] = None


Activity.update_forward_refs()

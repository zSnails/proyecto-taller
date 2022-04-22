from pydantic import BaseModel, ValidationError
from enum import IntEnum, auto
from datetime import date, time
from typing import List, Tuple, Optional

class Career(BaseModel):
    """Career class to be used by relationships"""

    id: int
    name: str

class WeekDays(IntEnum):
    MONDAY = auto()
    TUESDAY = auto()
    WEDNESDAY = auto()
    THURSDAY = auto()
    FRIDAY = auto()
    SATURDAY = auto()
    SUNDAY = auto()

class ReportType(IntEnum):
    DAILY = auto()
    WEEKLY = auto()

class Course(BaseModel):
    """Course class to be used by each account"""

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
    """AccountRole enum to be used by accounts"""

    STUDENT = auto()
    ADMIN = auto()


class Account(BaseModel):
    """Account class to be used by students"""

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
    id: int
    name: str
    belongs_to: int
    description: str
    course: Optional[int] = None
    activity_date: date
    done: bool
    start_hour: time
    end_hour: time
   

from dataclasses import dataclass
from enum import Enum, auto
from datetime import date, time
from typing import List, Tuple


class Career(dataclass):
    name: str


class Course(dataclass):
    """Course class to be used by each account"""

    name: str
    credit: int
    course_hours: int
    start_date: date
    end_date: date
    schedule: List[Tuple(date, time, time)]
    belongs_to: List[Career]

class AccountType(Enum):
    """AccountType enum to be used by accounts"""

    STUDENT = auto()
    ADMIN = auto()

class Account(dataclass):
    """Account class to be used by students"""

    name: str
    courses: List[Course]
    _type: AccountType

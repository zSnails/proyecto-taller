from pydantic import BaseModel
from enum import IntEnum, auto
from datetime import date, time
from typing import List, Tuple

class Career(BaseModel):
    """Career class to be used by relationships"""

    id: int
    name: str

class Course(BaseModel):
    """Course class to be used by each account"""

    id: int
    name: str
    credit: int
    course_hours: int
    start_date: date
    end_date: date
    # TODO: change the type for each schedule day to a binary number contaning
    # each of the 7 days of the week, it should be of type int, and the other
    # two values are fine
    schedule: List[Tuple[date, time, time]] = []
    belongs_to: List[int] = []

class AccountRole(IntEnum):
    """AccountRole enum to be used by accounts"""

    STUDENT = auto()
    ADMIN = auto()

class Account(BaseModel):
    """Account class to be used by students"""
    
    id: int
    name: str
    courses: List[int] = []
    career: int
    role: AccountRole

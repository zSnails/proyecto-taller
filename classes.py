from pydantic import BaseModel
from enum import Enum, auto
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
    schedule: List[Tuple[date, time, time]] = []
    belongs_to: List[str] = []

class AccountType(str, Enum):
    """AccountType enum to be used by accounts"""

    STUDENT = auto()
    ADMIN = auto()

class Account(BaseModel):
    """Account class to be used by students"""
    
    id: int
    name: str
    courses: List[Course] = []
    _type: AccountType

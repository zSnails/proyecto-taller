from typing import List
from enum import Enum, auto

class CommandCode(Enum):
    """CommandCode enum for internal command return value handling"""

    EXIT = auto()
    SUCCESS = auto()
    CONTINUE = auto()
    NOT_FOUND = auto()

class Command:
    """Command interface for internal command handling"""

    name: str
    aliases: List[str]
    def run(self) -> CommandCode: raise NotImplementedError

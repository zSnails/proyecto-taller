from typing import List
from enum import Enum, auto
from models import AccountRole


class CommandCode(Enum):
    """
    The commandcode enum represents the different command exit codes that might occur
    a command code is returned from a command, and it tells the program what to do based
    on the type of code
    """

    EXIT = auto()
    SUCCESS = auto()
    CONTINUE = auto()
    NOT_FOUND = auto()
    FORBIDDEN = auto()


class Command:
    """
    The command class is just an interface for a command implementation and is not
    to be used other than inherit from it
    """

    name: str
    aliases: List[str]
    description: str
    required_role: AccountRole

    def __init__(self):
        self.name = "default"
        self.aliases = []
        self.description = "Such a nice command!"
        self.required_role = AccountRole.STUDENT

    def run(self) -> CommandCode:
        raise NotImplementedError

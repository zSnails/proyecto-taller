from typing import List
from enum import Enum, auto
from models import AccountRole

class CommandCode(Enum):
    """CommandCode enum for internal command return value handling"""

    EXIT        = auto()
    SUCCESS     = auto()
    CONTINUE    = auto()
    NOT_FOUND   = auto()
    FORBIDDEN   = auto()

class Command:
    """Command interface for internal command handling"""
    
    name: str
    aliases: List[str]
    description: str
    required_role: AccountRole

    def __init__(self):
        self.name = "default"
        self.aliases = []
        self.description = "Such a nice command!"
        self.required_role = AccountRole.STUDENT

    def run(self) -> CommandCode: raise NotImplementedError

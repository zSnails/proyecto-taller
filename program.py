from command import Command, CommandCode
from typing import Optional, List, Union, Dict
from models import Account
from manager import Manager
from auth import Auth
from json import JSONDecodeError

class Program:
    def __init__(self, auth, manager, account):
        self.manager: Manager = manager
        # TODO: fix logging before initialization
        self.user: Account = account
        self.commands: Dict[str, Command] = {}
        self.aliases: Dict[str, Command] = {}
        self.auth: Auth = auth

    
    def get_command(self, name: str) -> Optional[Command]:
        command = self.commands.get(name)
        if not command:
            command = self.aliases.get(name)
        
        return command
      
    def load_command(self, command: Command):
        self.commands.setdefault(command.name, command)
        if command.aliases:
            for alias in command.aliases:
                self.aliases.setdefault(alias, command)

    def prompt(self) -> Union[Command, CommandCode]:
        user: str = self.user.name
        typ: str = self.user.role
        search_term: str = input(f"{user}::{typ}> ")

        if not search_term: return CommandCode.CONTINUE

        cmd: Command = self.get_command(search_term)
        if not cmd: return CommandCode.NOT_FOUND
        elif self.user.role < cmd.required_role: return CommandCode.FORBIDDEN
        else: return cmd.run(self)

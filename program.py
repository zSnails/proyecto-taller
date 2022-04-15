from command import Command, CommandCode
from typing import Optional, List, Union, Dict
from models import Account
from getpass import getpass
from manager import Manager
from auth import Auth
from json import JSONDecodeError

class Program:
    def __init__(self):
        self.manager: Manager = Manager()
        self.user: Account
        self.commands: Dict[str, Command] = {}
        self.auth: Auth = Auth()

        # TODO: find a better workaround
    def init(self):
        try:
            self.auth.load_data()
        except JSONDecodeError:
            self.commands.get('register-user').run()

    def login(self) -> bool:
        username = input("Username> ")
        password = getpass("Password> ")

        if self.auth.verify_account(username, password):
            self.user = self.manager.get_account(name=username)
            return True

        print("Either the username or the password is wrong")
        return False

    def load_command(self, command: Command):
        self.commands.setdefault(command.name, command)

    def prompt(self) -> Union[Command, CommandCode]:
        user: str = self.user.name
        typ: str = self.user.role
        search_term: str = input(f"{user}::{typ}> ")

        if not search_term: return CommandCode.CONTINUE

        cmd: Command = self.commands.get(search_term)
        if not cmd: return CommandCode.NOT_FOUND
        elif self.user.role < cmd.required_role: return CommandCode.FORBIDDEN
        else: return cmd.run()

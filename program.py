from command import Command, CommandCode
from typing import Optional, List
from classes import Account
from getpass import getpass
from manager import Manager
from auth import Auth


class Program:
    def __init__(self):
        self.manager: Manager = Manager()
        self.auth: Auth = Auth()
        self.user: Account
        self.commands: List[Command] = []

    def login(self) -> bool:
        username = input("Username> ")
        password = getpass("Password> ")

        if self.auth.verify_account(username, password):
            self.user = self.manager.get_account(name=username)
            return True

        print("Either the username or the password is wrong")
        return False

    def load_command(self, command: Command):
        self.commands.append(command)

    def get_command(self, search_term: str) -> Optional[Command]:
        for command in self.commands:
            if command.name == search_term or search_term in command.aliases:
                return command
        return None

    def prompt(self) -> CommandCode:
        user = self.user.name
        typ = self.user.role
        search_term = input(f"{user}::{typ}> ")

        cmd: Command = self.get_command(search_term)

        if cmd is None: return CommandCode.NOT_FOUND
        elif self.user.role < cmd.required_role: return CommandCode.FORBIDDEN
        else: return cmd.run()

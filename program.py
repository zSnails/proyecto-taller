from manager import Manager
from classes import Account
from auth import Auth
from getpass import getpass
from typing import Optional
from command import Command, CommandCode


class Program:
    def __init__(self):
        self.manager: Manager = Manager()
        self.auth: Auth = Auth()
        self.user: Account
        self.commands: List[Command] = []

    def login(self) -> Optional[Account]:
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

        cmd = self.get_command(search_term)

        if cmd:
            return cmd.run()

        return CommandCode.NOT_FOUND


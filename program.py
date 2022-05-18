from command import Command, CommandCode
from typing import Optional, List, Union, Dict
from models import Account
from manager import Manager
from colorama import Fore, Style
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
        """
        The get command function tries to find a command by its name or an alias
        it first tries to search for the command in the commands dictionary, if
        it can't find it there then it tries to find it in the aliases dictionary

        Parameters
        ----------
            -    name: The name of a command to look for

        Returns
        -------
            -    Command: A command instance that can be run
        """
        command = self.commands.get(name)
        if not command:
            command = self.aliases.get(name)

        return command

    def load_command(self, command: Command):
        """
        The load command function loads commands into the commands dictionary,
        and also sets their aliases

        Parameters
        ----------
            -   command: A command instance to be loaded into the commands and aliases dictionaries

        Returns
        -------
            -   None
        """
        self.commands.setdefault(command.name, command)
        if command.aliases:
            for alias in command.aliases:
                self.aliases.setdefault(alias, command)

    def prompt(self) -> Union[Command, CommandCode]:
        """
        The prompt function is responsible for getting user input, all user input goes
        through the prompt function

        Parameters
        ----------
            -   None

        Returns:
            - Command: if the command lookup was sucessful it returns a command instance
            - CommandCode: if the command lookup was unsucessful it returns a CommandCode.NOT_FOUND
        """

        user: str = self.user.name
        typ: str = self.user.role

        search_term: str = input(f"{Fore.CYAN}{user}{Style.RESET_ALL}::{typ}> ")

        if not search_term:
            return CommandCode.CONTINUE

        cmd: Command = self.get_command(search_term)

        if not cmd:
            return CommandCode.NOT_FOUND
        elif self.user.role < cmd.required_role:
            return CommandCode.FORBIDDEN
        else:
            return cmd.run(self)

from program import Program, CommandCode
from os import listdir
from importlib import import_module

def main():
    command_modules = listdir("./commands")
    p = Program()

    for cmd in command_modules:
        if cmd in ('__init__.py', '__pycache__'): continue
        import_module(f"commands.{cmd[0:-3]}").setup(p)

    logged_in = False
    while not logged_in:
        logged_in = p.login()

    while True:
        code = p.prompt()

        # handle command exit codes
        if code == CommandCode.EXIT:
            break
        elif code == CommandCode.NOT_FOUND:
            print("Command not found")
        elif code == CommandCode.FORBIDDEN:
            print("You can't use that command")

if __name__ == '__main__':
    main()

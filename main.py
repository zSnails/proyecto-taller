from program import Program, CommandCode
from os import listdir
from importlib import import_module

def main():
    command_modules = listdir("./commands")
    p = Program()

    for cmd in command_modules:
        if cmd in ('__init__.py', '__pycache__'): continue
        # import_module(f"..{cmd}", package="commands.subpkg").setup(p)
        import_module(f"commands.{cmd[0:-3]}").setup(p)

    logged_in = False
    while not logged_in:
        logged_in = p.login()

    is_running = True
    while is_running:
        code = p.prompt()

        # handle command exit codes
        if code == CommandCode.EXIT:
            is_running = False
        elif code == CommandCode.NOT_FOUND:
            print("Command not found")

if __name__ == '__main__':
    main()

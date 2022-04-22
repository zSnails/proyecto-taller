from command import Command, CommandCode
from program import Program
from colorama import Fore, Style

class ShowProfileCommand(Command):
    def __init__(self):
        super().__init__()
        self.name = "show-profile"
        self.aliases = ["sp", "shp"]

    def run(self, ctx: Program) -> CommandCode:
        
        print("Showing your information")
        
        
        # Base info
        print(f"{Fore.GREEN}Name{Style.RESET_ALL}: {ctx.user.name}\n{Fore.GREEN}Phone number{Style.RESET_ALL}: {ctx.user.phone_number}")
        
        # Technical info
        print(f"{Fore.YELLOW}Id{Style.RESET_ALL}: {ctx.user.id}\n{Fore.YELLOW}Role{Style.RESET_ALL}: {ctx.user.role}")
        
        # Career info
        
        career = ctx.manager.get_career(id=ctx.user.career)
        
        print(f"{Fore.BLUE}Career{Style.RESET_ALL}: {career.name}")
        
        courses = ctx.manager.get_courses(career_id=ctx.user.career)
        print(f"{Fore.MAGENTA}Courses{Style.RESET_ALL}:")
        for course in courses:
            end = ""
            if course.id in ctx.user.passed:
                end = f"{Fore.GREEN}- passed{Style.RESET_ALL}"
            elif course.id in ctx.user.failed:
                end = f"{Fore.RED}- failed{Style.RESET_ALL}"
            
            print(f"\t- {course.name}", end)       
        
        return CommandCode.SUCCESS

def setup(program):
    program.load_command(ShowProfileCommand())
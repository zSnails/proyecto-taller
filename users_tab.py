from tkinter.ttk import Frame, Button, OptionMenu, Label, Entry
from tkinter.messagebox import showerror
from tkinter import Text, StringVar, Tk, Listbox
from models import AccountRole, Account, ReportType


class UsersTab(Frame):
    """
    The UsersTab class instantiates a tab in the main window
    """
    def __init__(self, program):
        super().__init__()
        self.name = "Users"
        self.program = program

        self.initUI()

    def initUI(self):
        """
        Initializes the main ui of the current tab

        Parameters
        ----------
            -   None

        Returns
        -------
            -   None
        """
        self.pack(fill="both", expand=True)

        self.columnconfigure(1, weight=1)
        self.columnconfigure(3, pad=7)
        self.rowconfigure(3, weight=1)
        self.rowconfigure(5, pad=7)

        self.seleccionado = StringVar()
        self.available_accounts = [
            account.name for account in self.program.manager.accounts
        ]
        self.disponibles = OptionMenu(
            self, self.seleccionado, "None", *self.available_accounts
        )
        self.disponibles.grid(sticky="w", pady=4, padx=5)

        if self.program.user.role == AccountRole.ADMIN:
            self.btn_nuevo = Button(self, text="Nuevo", command=self.new_user)
            self.btn_nuevo.grid(row=1, column=3)

        self.btn_ver = Button(self, text="Ver", command=self.show_data)
        self.btn_ver.grid(row=2, column=3)

        self.area = Text(self)
        self.area.grid(
            row=1, column=0, columnspan=2, rowspan=4, padx=5, sticky="ewsn"
        )
        self.area.configure(state="disabled")

    def new_user(self):
        """
        User creation helper, creates a modal for user creation
        """
        modal = Tk()
        modal.wm_title("Register user")
        name_label = Label(modal, text="Name").grid(row=0, column=0)
        name_entry = Entry(modal)
        name_entry.grid(row=0, column=1)

        role_label = Label(modal, text="Role").grid(row=1, column=0)
        selected_role = StringVar()
        role_menu = OptionMenu(
            modal, selected_role, "Admin", "Admin", "Student"
        )
        role_menu.grid(row=1, column=1)

        selected_report = StringVar()
        report_label = Label(modal, text="Report type").grid(row=3, column=0)
        report_menu = OptionMenu(
            modal, selected_report, "Daily", "Daily", "Weekly"
        )
        report_menu.grid(row=3, column=1)

        phone_number_label = Label(modal, text="Phone number (optional)").grid(
            row=4, column=0
        )
        phone_number_entry = Entry(modal)
        phone_number_entry.grid(row=4, column=1)

        selected_career = StringVar()
        career_label = Label(modal, text="Career").grid(row=5, column=0)
        careers = [career.name for career in self.program.manager.careers]
        career_menu = OptionMenu(modal, selected_career, "None", *careers)
        career_menu.grid(row=5, column=1)

        course_label = Label(modal, text="Course").grid(row=6, column=0)
        course_menu = Listbox(modal, selectmode="multiple")
        course_menu.grid(row=6, column=1)

        def update_courses(*_):
            """
            Helper function for updating courses, meant for internal use
            """
            career = self.program.manager.get_career(name=selected_career.get())
            course_menu.delete(0, "end")
            for course in self.program.manager.get_courses(career_id=career.id):
                course_menu.insert("end", course.name)

        password_label = Label(modal, text="Password").grid(row=7, column=0)
        password_entry = Entry(modal)
        password_entry.grid(row=7, column=1)

        _pass_label = Label(modal, text="Confirm password").grid(
            row=8, column=0
        )
        _pass_entry = Entry(modal)
        _pass_entry.grid(row=8, column=1)

        selected_career.trace("w", update_courses)

        def register_user():
            """
            Helper function for user registration, meant for internal use
            """
            career = self.program.manager.get_career(name=selected_career.get())
            if career:
                courses = [
                    course.id
                    for course in self.program.manager.get_courses(
                        career_id=career.id
                    )
                    if course.name in course_menu.selection_get().split("\n")
                ]

            usr = Account(
                id=len(self.program.manager.accounts) + 1,
                name=name_entry.get(),
                role=AccountRole[selected_role.get().upper()],
                career=career.id if career else 0,
                reports=ReportType[selected_report.get().upper()],
                phone_number=phone_number_entry.get(),
                courses=courses,
            )

            if password_entry.get() != _pass_entry.get():
                showerror(
                    title="Coulnd't register user",
                    message="The passwords do not match",
                )
                return

            self.program.manager.register_user(usr)
            self.program.auth.store_password(usr.name, password_entry.get())
            modal.destroy()

        Button(modal, text="Register", command=register_user).grid(
            row=9, column=1
        )
        modal.mainloop()

    def show_data(self):
        """
        Updates the main text area, meant for internal use
        """
        user = self.program.manager.get_account(name=self.seleccionado.get())
        if not user:
            return

        career = self.program.manager.get_career(id=self.program.user.career)

        courses = "Courses: \n"
        for course in self.program.manager.get_courses(career_id=user.career):
            end = ""
            if course.id not in user.courses:
                continue
            if course.id in user.passed:
                end = "- passed"
            if course.id in user.failed:
                end = "- failed"
            courses += f" - {course.name} {end}\n"

        text = (
            f"ID: {user.id}\n"
            f"Name: {user.name}\n"
            f"Career: {career.name if career else career}\n{courses}"
        )
        self.area.configure(state="normal")
        self.area.delete(1.0, "end")
        self.area.insert(1.0, text)
        self.area.configure(state="disabled")

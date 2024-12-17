from tkinter.ttk import Frame, Button, OptionMenu, Label, Entry
from tkinter import Text, StringVar, Tk
from tkinter.messagebox import showinfo
from models import Career, AccountRole


class CareersTab(Frame):
    def __init__(self, program):
        super().__init__()
        self.name = "Careers"
        self.program = program
        self.initUI()

    def initUI(self):
        """
        Initializes the current tab to be used in the main window
        """
        self.pack(fill="both", expand=True)

        self.columnconfigure(1, weight=1)
        self.columnconfigure(3, pad=7)
        self.rowconfigure(4, weight=1)
        self.rowconfigure(5, pad=7)

        self.careers = ["None"] + [
            career.name for career in self.program.manager.careers
        ]

        self.selected = StringVar()
        self.available = OptionMenu(self, self.selected, *self.careers)
        self.available.grid(sticky="w", pady=4, padx=5)
        if self.program.user.role == AccountRole.ADMIN:
            self.new_button = Button(self, text="New", command=self.new_career)
            self.new_button.grid(row=1, column=3)

        self.text_area = Text(self)
        self.text_area.configure(state="disabled")
        self.text_area.grid(
            row=1, column=0, columnspan=2, rowspan=4, padx=5, sticky="ewsn"
        )

        self.view_button = Button(self, text="View", command=self.view_career)
        self.view_button.grid(row=2, column=3)

        self.switch_button = Button(self, text="Switch", command=self.switch_career)
        self.switch_button.grid(row=3, column=3)

    def view_career(self):
        """
        Updates the main textbox and shows relevant career info /s
        """
        career = self.selected.get()
        self.text_area.configure(state="normal")
        self.text_area.delete(1.0, "end")
        self.text_area.insert(1.0, career)
        self.text_area.configure(state="disabled")

    def switch_career(self):
        """
        This shows the career switching modal, nothing more
        """
        modal = Tk()
        # available = [career.name for career in self.program.manager.careers]
        selected = StringVar()
        careers = OptionMenu(
            modal,
            selected,
            *(["None"] + self.careers),
        )
        careers.grid(row=0, column=0)

        def switch_career():
            """
            Helper function for switching career, meant for internal use
            """
            career = self.program.manager.get_career(selected.get())

            if not career:
                return

            self.program.manager.switch_account_career(
                account_id=self.program.user.id, career_id=career.id
            )
            self.program.manager.reset_account_courses(account_id=self.program.user.id)
            self.program.user = self.program.manager.get_account(
                id=self.program.user.id
            )
            showinfo(title="Succes", message=f"Switched to career '{career.name}'")
            modal.destroy()

        switch_button = Button(modal, text="switch", command=switch_career)
        switch_button.grid(row=0, column=1)

        modal.mainloop()

    def new_career(self):
        """
        Creates and shows the career registration modal
        """
        modal = Tk()
        modal.title("Register career")

        name_label = Label(modal, text="Name").grid(row=0, column=0, pady=5)
        name_entry = Entry(modal)
        name_entry.grid(row=0, column=1, pady=5)

        def register_career():
            """
            Helper function for career registration, meant for internal use
            """

            name = name_entry.get()
            if not name:
                return

            self.program.manager.register_career(
                Career(id=len(self.program.manager.careers) + 1, name=name)
            )

            showinfo(title="Success", message=f"Created career '{name}'")
            modal.destroy()

        register_btn = Button(modal, text="Register", command=register_career)
        register_btn.grid(row=1, column=1, pady=3)

        modal.mainloop()

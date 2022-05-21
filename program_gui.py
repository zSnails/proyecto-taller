from tkinter import Tk
from tkinter.ttk import Notebook


class Program(Tk):
    def __init__(self, auth, manager, account, tabs=[]):
        super().__init__()
        self.manager = manager
        self.user = account
        self.auth = auth

        self.wm_title("Time management program")
        self.wm_minsize(width=600, height=300)

        self.notebook = Notebook(self)

        for tab in tabs:
            t = tab(self)
            self.notebook.add(t, text=t.name)

        self.notebook.pack(expand=True, fill="both")

    def run(self):
        return self.mainloop()

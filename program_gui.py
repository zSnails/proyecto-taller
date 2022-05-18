from tkinter import Tk
from tkinter.ttk import Notebook


class Program(Tk):
    def __init__(self, auth, manager, account, tabs=[]):
        super().__init__()
        self.__manager = manager
        self.__user = account
        self.__auth = auth

        self.wm_title("Time management program")
        self.wm_minsize(width=600, height=300)

        self.notebook = Notebook(self)

        for tab in tabs:
            t = tab()
            self.notebook.add(t, text=t.name)
            
        self.notebook.pack(expand=True, fill="both")


    def run(self):
        return self.mainloop()

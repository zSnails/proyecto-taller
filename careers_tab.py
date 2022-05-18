from tkinter.ttk import Frame, Button, OptionMenu, Label
from tkinter import Text


class CareersTab(Frame):
    def __init__(self):
        super().__init__()
        self.name = "Careers"

        self.initUI()

    def initUI(self):
        self.pack(fill="both", expand=True)

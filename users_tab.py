from tkinter.ttk import Frame, Button, OptionMenu, Label
from tkinter import Text, StringVar


class UsersTab(Frame):
    def __init__(self):
        super().__init__()
        self.name = "Users"

        self.initUI()

    def initUI(self):
        self.pack(fill="both", expand=True)

        self.columnconfigure(1, weight=1)
        self.columnconfigure(3, pad=7)
        self.rowconfigure(3, weight=1)
        self.rowconfigure(5, pad=7)

        self.seleccionado = StringVar()
        self.disponibles = OptionMenu(
            self,
            self.seleccionado,
            *[
                "Ninguno",
                "me cago en samuel",
                "putos negros odio a los negros los considero la raza inferior y",
            ]
        )
        self.disponibles.grid(sticky="w", pady=4, padx=5)
        self.btn_nuevo = Button(self, text="Nuevo")
        self.btn_nuevo.grid(row=1, column=3)

        self.btn_ver = Button(self, text="Ver", command=self.show_data)
        self.btn_ver.grid(row=2, column=3)

        self.area = Text(self)
        self.area.grid(row=1, column=0, columnspan=2, rowspan=4, padx=5, sticky="ewsn")

    def show_data(self):
        pass

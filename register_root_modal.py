from tkinter import Tk, Label, StringVar, Entry, Button
from functools import partial
from models import Account, AccountRole


def register(manager, auth, name, password, confirm, widget):
    password = password.get()
    confirm = confirm.get()

    if password == confirm:
        usr = Account(
            id=len(manager.accounts) + 1,
            name=name.get(),
            role=AccountRole.ADMIN,
            career=0,
            courses=[],
            passed=[],
            failed=[],
            reports=1,
            activities=[],
        )
        manager.register_user(usr)
        auth.store_password(usr.name, password)
        widget.destroy()


def register_root_user_modal(manager, auth):
    modal_window = Tk()
    modal_window.wm_title("Register root user")
    modal_window.grid_rowconfigure(0, pad=5)
    name_label = Label(modal_window, text="Username")
    name_label.grid(row=0, column=0)
    username = StringVar()

    name_entry = Entry(modal_window, textvariable=username)
    name_entry.grid(row=0, column=1)

    pass_label = Label(modal_window, text="Password")
    pass_label.grid(row=1, column=0)
    password = StringVar()
    pass_entry = Entry(modal_window, textvariable=password, show="*")
    pass_entry.grid(row=1, column=1)

    confirm_label = Label(modal_window, text="Confirm Password")
    confirm_label.grid(row=2, column=0)
    confirm = StringVar()
    confirm_entry = Entry(modal_window, textvariable=confirm, show="*")
    confirm_entry.grid(row=2, column=1)

    register_f = partial(
        register, manager, auth, username, password, confirm, modal_window
    )

    register_button = Button(modal_window, text="Register", command=register_f)
    register_button.grid(row=4, column=0)

    modal_window.mainloop()

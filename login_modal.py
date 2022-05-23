from tkinter import Tk, Label, StringVar, Entry, Button
from functools import partial
from models import Account, AccountRole


def validate_user(widget, auth, name, passwd):
    """
    The validate user function validates the current user trying to login
    Meant for internal use
    """
    if auth.verify_account(name.get(), passwd.get()):
        widget.destroy()


def login_modal(auth):
    """
    Creates and shows the login modal window
    Meant for internal use
    """
    modal_window = Tk()
    modal_window.wm_title("Login")
    modal_window.grid_rowconfigure(0, pad=5)
    modal_window.protocol("WM_DELETE_WINDOW", exit)
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

    validator = partial(validate_user, modal_window, auth, username, password)

    login_button = Button(modal_window, text="Login", command=validator)
    login_button.grid(row=2, column=0)
    modal_window.mainloop()

    return username.get()

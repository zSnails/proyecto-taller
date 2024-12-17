from tkinter import Tk, StringVar, Text, Listbox
from tkinter.ttk import Label, Button, Entry, OptionMenu, Frame
from arrow import get
from datetime import datetime
from tkcalendar import DateEntry
from models import Activity


class ActivitiesTab(Frame):
    """
    The ActivitiesTab class instantiates a tab in the main window
    """

    def __init__(self, program):
        super().__init__()
        self.name = "Activities"
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
        self.rowconfigure(4, weight=1)
        self.rowconfigure(5, pad=7)

        self.update_activities()

        self.selected = StringVar()
        self.available = OptionMenu(self, self.selected, *self.activities)
        self.available.grid(sticky="w", pady=4, padx=5)

        self.text_area = Text(self)
        self.text_area.configure(state="disabled")
        self.text_area.grid(
            row=1, column=0, columnspan=2, rowspan=4, padx=5, sticky="ewsn"
        )

        self.new_button = Button(self, text="New", command=self.new_activity)
        self.new_button.grid(row=1, column=3)

        self.view_button = Button(self, text="View", command=self.view_activity)
        self.view_button.grid(row=2, column=3)
        self.mark_button = Button(
            self, text="Toggle status", command=self.update_activity_status
        )
        self.mark_button.grid(row=3, column=3)

    def update_activity_status(self):
        """
        Helper function for updating activitiy statuses, meant for internal
        """
        activity = self.program.manager.get_activity(name=self.selected.get())
        if not activity:
            return
        self.program.manager.update_activity(activity.id)

    def update_activities(self):
        """
        Helper function for updating activities, meant for internal use
        """
        self.activities = ["None"] + [
            activity.name
            for activity in self.program.manager.get_activities()
            if activity.id in self.program.user.activities
        ]

    def new_activity(self):
        """
        Activity creation helper, creates a modal for user creation
        """
        modal = Tk()
        modal.title("Register new activity")
        name_label = Label(modal, text="Name").grid(row=0, column=0)
        name_entry = Entry(modal)
        name_entry.grid(row=0, column=1)

        description_label = Label(modal, text="Description").grid(row=1, column=0)
        description_entry = Entry(modal)
        description_entry.grid(row=1, column=1)

        course_select_label = Label(modal, text="Course to bind to").grid(
            row=2, column=0
        )
        available_courses = Listbox(modal, selectmode="single")
        available_courses.grid(row=2, column=1)
        [
            available_courses.insert("end", course.name)
            for course in self.program.manager.get_courses(
                career_id=self.program.user.career
            )
            if course.id in self.program.user.courses
        ]

        activity_date_label = Label(modal, text="Date").grid(row=3, column=0)
        activity_date_entry = DateEntry(modal)
        activity_date_entry.grid(row=3, column=1)

        activity_start_time_label = Label(modal, text="Start time").grid(
            row=4, column=0
        )
        activity_start_time_entry = Entry(modal)
        activity_start_time_entry.grid(row=4, column=1)

        activity_end_time_label = Label(modal, text="End time").grid(row=5, column=0)
        activity_end_time_entry = Entry(modal)
        activity_end_time_entry.grid(row=5, column=1)

        def register_activity():
            """
            Helper function for user registration, meant for internal use
            """
            try:
                course = self.program.manager.get_course(
                    available_courses.selection_get()
                )
            except:
                course = None
            activity = Activity(
                id=len(self.program.manager.activities) + 1,
                name=name_entry.get(),
                belongs_to=self.program.user.id,
                description=description_entry.get(),
                course=course.id if course else course,
                activity_date=activity_date_entry.get_date(),
                done=False,
                start_hour=datetime.strptime(
                    activity_start_time_entry.get(), "%H:%M:%S"
                ).time(),
                end_hour=datetime.strptime(
                    activity_end_time_entry.get(), "%H:%M:%S"
                ).time(),
            )
            self.program.manager.add_activity_to_user(activity.id, self.program.user.id)
            self.program.manager.register_activity(activity)

        Button(modal, text="Register", command=register_activity).grid(row=6, column=1)

        self.update_activities()
        modal.mainloop()

    def view_activity(self):
        """
        Updates the main text area, meant for internal use
        """
        activity = self.program.manager.get_activity(name=self.selected.get())
        if not activity:
            return

        self.text_area.configure(state="normal")
        self.text_area.delete(1.0, "end")
        text = (
            f"ID: {activity.id}\n"
            f"Name: {activity.name}\n"
            f"Date: {get(activity.activity_date).humanize()}\n"
            f"Description: {activity.description}\n"
            f"Status: {'done' if activity.done else 'unfinished'}"
        )
        self.text_area.insert(1.0, text)
        self.text_area.configure(state="disabled")

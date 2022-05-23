from tkinter.ttk import Frame, Button, OptionMenu, Label, Entry
from tkcalendar import DateEntry
from tkinter import Text, StringVar, Tk, Listbox
from tkinter.messagebox import showinfo
from functools import partialmethod
from models import WeekDays, Course
from datetime import datetime
from models import AccountRole


class CoursesTab(Frame):
    def __init__(self, program):
        super().__init__()
        self.name = "Courses"
        self.program = program
        self.initUI()

    def initUI(self):
        """
        Creates the courses tab in the main window
        """
        self.pack(fill="both", expand=True)

        self.columnconfigure(1, weight=1)
        self.columnconfigure(3, pad=7)
        self.rowconfigure(4, weight=1)
        self.rowconfigure(5, pad=7)

        self.seleccionado = StringVar()
        self.update_courses()

        self.disponibles = OptionMenu(
            self, self.seleccionado, "None", *self.courses
        )
        self.disponibles.grid(sticky="w", pady=4, padx=5)

        if self.program.user.role == AccountRole.ADMIN:
            self.new_button = Button(
                self, text="New", command=self.new_course_tab
            )
            self.new_button.grid(row=1, column=3)

        self.view_button = Button(self, text="View", command=self.show_data)
        self.view_button.grid(row=2, column=3)

        self.btn_join = Button(
            self, text="Join Course", command=self.join_course
        )
        self.btn_join.grid(row=3, column=3)

        self.text_area = Text(self)
        self.text_area.configure(state="disabled")
        self.text_area.grid(
            row=1, column=0, columnspan=2, rowspan=4, padx=5, sticky="ewsn"
        )

    def update_courses(self):
        """
        Helper function to update courses, meant for internal use
        """
        self.courses = [
            course.name
            for course in self.program.manager.get_account_courses(
                id=self.program.user.id
            )
        ]

    def join_course(self):
        """
        Creates and shows the course joining modal
        """
        modal = Tk()
        available_courses = [
            f"{course.name}"
            for course in self.program.manager.get_courses(
                self.program.user.career
            )
            if course.id not in self.program.user.courses
        ]
        selected = StringVar()
        available = OptionMenu(modal, selected, *["None"] + available_courses)
        available.grid(row=0, column=0)

        def join_course():
            """
            Helper function for joining courses, meant for internal use
            """
            course = self.program.manager.get_course(name=selected.get())
            if not course:
                return

            self.program.manager.update_account_courses(
                course.id, account_id=self.program.user.id
            )
            self.program.user = self.program.manager.get_account(
                id=self.program.user.id
            )

            self.update_courses()
            modal.destroy()

        join_button = Button(modal, text="Join", command=join_course)
        join_button.grid(row=0, column=1)

    def show_data(self):
        """
        Helper function to show course data, updates the main textbox to show
        relevant data
        """
        course = self.program.manager.get_course(name=self.seleccionado.get())
        if not course:
            return

        self.text_area.configure(state="normal")
        self.text_area.delete(1.0, "end")
        text = (
            f"Name: {course.name}\n"
            f"Status: {'passed' if course.id in self.program.user.passed else 'not passed'}\n"
            f"Credits: {course.credits}\n"
            f"Course hours: {abs(course.course_hours)}\n"
            f"Weekly Hours: {course.weekly_hours}\n"
            f"Start Date: {course.start_date}\n"
            f"End Date: {course.end_date}"
        )

        # for day, begin, end in course.schedule:

        self.text_area.insert(1.0, text)
        self.text_area.configure(state="disabled")

    def new_course_tab(self):
        """
        Creates and shows the course creation modal window
        """
        modal = Tk()
        modal.title("Register new course")
        name_label = Label(modal, text="Course name").grid(row=0, column=0)
        name_entry = Entry(modal)
        name_entry.grid(row=0, column=1)

        credits_label = Label(modal, text="Course credits").grid(
            row=1, column=0
        )
        credits_entry = Entry(modal)
        credits_entry.grid(row=1, column=1)

        start_date_label = Label(modal, text="Start Date").grid(row=2, column=0)
        start_date_calendar = DateEntry(modal, selectmode="day")
        start_date_calendar.grid(row=2, column=1)

        end_date_label = Label(modal, text="Start Date").grid(row=3, column=0)
        end_date_calendar = DateEntry(modal, selectmode="day")
        end_date_calendar.grid(row=3, column=1)

        schedule = []
        course_hours = 0
        self.weekly_hours = 0
        weekdays_list = ["None"] + [
            str(day).split(".").pop() for day in WeekDays
        ]
        selected_day = StringVar()
        days_listbox = OptionMenu(modal, selected_day, *weekdays_list)
        days_listbox.grid(row=4, column=1)

        begin_label = Label(modal, text="Begin hour (h:m:s format)").grid(
            row=5, column=0
        )
        begin_entry = Entry(modal)
        begin_entry.grid(row=5, column=1)

        end_label = Label(modal, text="End hour (h:m:s format)").grid(
            row=6, column=0
        )
        end_entry = Entry(modal)
        end_entry.grid(row=6, column=1)

        def append_to_schedule():
            """
            Helper function to append a day to the schedule, meant for internal use
            """
            begin = datetime.strptime(begin_entry.get(), "%H:%M:%S")
            end = datetime.strptime(end_entry.get(), "%H:%M:%S")
            print(selected_day.get())

            schedule.append(
                (WeekDays[selected_day.get()], begin.time(), end.time())
            )
            self.weekly_hours += (end - begin).total_seconds() / 3600

        append_schedule_button = Button(
            modal, command=append_to_schedule, text="Add to schedule"
        )

        append_schedule_button.grid(row=7, column=1)

        career_selector_label = Label(modal, text="Career availability").grid(
            row=8, column=0
        )

        self.all_careers = self.program.manager.get_careers()
        career_selector = Listbox(modal, selectmode="multiple")
        career_selector.grid(row=8, column=1)
        [
            career_selector.insert("end", career.name)
            for career in self.all_careers
        ]

        def register_course():
            """
            Helper function for course registration, meant for internal use
            """
            available_careers = []
            for career in career_selector.selection_get().split("\n"):
                available_careers.append(
                    self.program.manager.get_career(name=career).id
                )

            course_duration = (
                start_date_calendar.get_date() - end_date_calendar.get_date()
            )
            course_hours = (course_duration.days // 30) * (
                self.weekly_hours * 4
            )
            course = Course(
                id=len(self.program.manager.courses) + 1,
                name=name_entry.get(),
                credits=int(credits_entry.get()),
                course_hours=course_hours,
                start_date=start_date_calendar.get_date(),
                end_date=end_date_calendar.get_date(),
                schedule=schedule,
                belongs_to=available_careers,
                weekly_hours=self.weekly_hours,
            )
            self.program.manager.register_course(course)
            showinfo(title="Success", message="Course created")
            self.update_courses()
            modal.destroy()

        register_button = Button(
            modal, text="Register", command=register_course
        )
        register_button.grid(row=9, column=1)

        modal.mainloop()

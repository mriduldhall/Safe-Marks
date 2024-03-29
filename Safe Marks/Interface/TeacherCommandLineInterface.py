from HelperLibrary.Validator import Validator
from HelperLibrary.Student import Student
from HelperLibrary.StorageFunctions import StorageFunctions
from Interface.SettingsCommandLineInterface import CLI as SettingsCLI
from Interface.AccountCommandLineInterface import CLI as AccountCLI

from datetime import datetime


class LogoutMenuItem:
    def __init__(self):
        self.is_exit_initiated = False

    def execute(self):
        print("Logging out...")
        self.is_exit_initiated = True

    def exit_initiated(self):
        return self.is_exit_initiated


class SettingsMenuItem:
    def __init__(self, singleton):
        self.singleton = singleton
        self.is_exit_initiated = False

    def execute(self):
        user_deleted = SettingsCLI(self.singleton).initiate()
        if user_deleted:
            self.is_exit_initiated = True

    def exit_initiated(self):
        return self.is_exit_initiated


class YearEndMenuItem:
    def __init__(self):
        pass

    def execute(self):
        if Validator("year end").should_continue():
            student_list = self.get_student_list()
            self.increase_year(student_list)

    @staticmethod
    def get_student_list():
        student_list = StorageFunctions("students").list("name")
        return student_list

    @staticmethod
    def increase_year(student_list):
        for student_name in student_list:
            student = Student(student_name, None, None, None, None)
            student.recreate_student()
            if not student.leave_date:
                if student.year_group != 13:
                    student.year_group += 1
                    student.student_controller.save_student_data(save_mark_sheet_data=False)
                    student.student_controller.create_mark_sheets()
                else:
                    student.year_group = None
                    student.leave_date = datetime.now()
                    student.student_controller.save_student_data(save_mark_sheet_data=False)

    @staticmethod
    def exit_initiated():
        return False


class ManageMenuItem:
    def __init__(self, admin):
        self.admin = admin

    def execute(self):
        if Validator("manage").should_continue():
            work_on_new_student = True
            while work_on_new_student:
                message = Student(None, None, None, None, None).manage(self.admin)
                print(message)
                work_on_new_student = bool(int(input("Enter 1 to enter another name and work on another student or 0 to leave.")))

    @staticmethod
    def exit_initiated():
        return False


class ManageAccountsMenuItem:
    def __init__(self, singleton):
        self.singleton = singleton

    def execute(self):
        AccountCLI(self.singleton).initiate()

    @staticmethod
    def exit_initiated():
        return False


class CreateMenuItem:
    def __init__(self, singleton):
        self.singleton = singleton

    def execute(self):
        if Validator("create").should_continue():
            continuation = True
            while continuation is True:
                menu_options = {
                    "1": self.new_student,
                    "2": self.old_student,
                }
                menu_choice = input("Enter 1 to create a new student or 2 to add an old student back(unarchive):")
                if menu_choice in menu_options.keys():
                    message = menu_options[menu_choice]()
                else:
                    message = "Invalid choice"
                print(message)
                continuation = bool(int(input("Enter 1 to create another student and 0 to head back to main menu.")))

    def new_student(self):
        student = self.getstudentdetails()
        return student.create_new_student()

    @staticmethod
    def old_student():
        return Student(None, None, None, None, None).create_old_student()

    @staticmethod
    def getstudentdetails():
        valid = False
        while not valid:
            name = input("Enter student's name:").capitalize()
            birth_year = int(input("Enter student's year of birth:"))
            birth_month = int(input("Enter student's month of birth:"))
            birth_date = int(input("Enter student's date of birth:"))
            date_of_birth = datetime(birth_year, birth_month, birth_date)
            address = input("Enter student's address:")
            father_name = input("Enter student's father's name:")
            mother_name = input("Enter student's mother's name:")
            student = Student(name, date_of_birth, address, father_name, mother_name)
            valid, message = student.student_controller.validate_student_details()
            if message:
                print(message)
        return student

    @staticmethod
    def exit_initiated():
        return False


class CLI:
    def __init__(self, singleton):
        self.main_menu_dictionary = {
            "m": ManageMenuItem(singleton.admin),
            "s": SettingsMenuItem(singleton),
            "l": LogoutMenuItem()
        }
        self.admin_main_menu_dictionary = {
            "c": CreateMenuItem(singleton),
            "m": ManageMenuItem(singleton.admin),
            "a": ManageAccountsMenuItem(singleton),
            "y": YearEndMenuItem(),
            "s": SettingsMenuItem(singleton),
            "l": LogoutMenuItem()
        }
        self.disabled_main_menu_dictionary = {
            "s": SettingsMenuItem(singleton),
            "l": LogoutMenuItem(),
        }
        self.admin = singleton.admin
        self.enabled = singleton.enabled

    def initiate(self):
        exit_initiated = False
        while not exit_initiated:
            if not self.enabled:
                print("Your account has been marked disabled. Please contact an administrator to get this changed.")
                choice = input("Enter s for settings and l to logout:").lower()
                menu_item = self.disabled_main_menu_dictionary.get(choice)
            elif not self.admin:
                choice = input("Enter m to manage students and their mark sheets, s for settings and l to logout:").lower()
                menu_item = self.main_menu_dictionary.get(choice)
            else:
                choice = input("Enter c to create new students, m to manage students and their mark sheets, a to manage accounts, y to change academic year, s for settings and l to logout:").lower()
                menu_item = self.admin_main_menu_dictionary.get(choice)
            if menu_item is None:
                print("Please enter valid choice")
                continue
            menu_item.execute()
            exit_initiated = menu_item.exit_initiated()

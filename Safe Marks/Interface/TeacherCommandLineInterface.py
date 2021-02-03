from HelperLibrary.Validator import Validator
from HelperLibrary.Student import Student
from Interface.SettingsCommandLineInterface import CLI as SettingsCLI


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


class ManageMenuItem:
    def __init__(self):
        pass

    @staticmethod
    def execute():
        if Validator("manage").should_continue():
            work_on_new_student = True
            while work_on_new_student:
                message = Student(None, None, None, None).manage()
                print(message)
                work_on_new_student = bool(int(input("Enter 1 to enter another name and work on another student or 0 to leave.")))

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
                student = self.getstudentdetails()
                message = student.create()
                print(message)
                continuation = bool(int(input("Enter 1 to create another student and 0 to head back to main menu.")))

    @staticmethod
    def exit_initiated():
        return False

    def getstudentdetails(self):
        name = input("Enter student's name:").capitalize()
        age = input("Enter student's age:")
        year_group = input("Enter student's year group:")
        student = Student(name, age, year_group, teacher=self.singleton.name)
        return student


class CLI:
    def __init__(self, singleton):
        self.main_menu_dictionary = {
            "m": ManageMenuItem(),
            "s": SettingsMenuItem(singleton),
            "l": LogoutMenuItem()
        }
        self.admin_main_menu_dictionary = {
            "c": CreateMenuItem(singleton),
            "m": ManageMenuItem(),
            "s": SettingsMenuItem(singleton),
            "l": LogoutMenuItem()
        }
        self.admin = singleton.admin

    def initiate(self):
        exit_initiated = False
        while not exit_initiated:
            if not self.admin:
                choice = input("Enter m to manage students and their mark sheets, s for settings and l to logout:")
                menu_item = self.main_menu_dictionary.get(choice)
            else:
                choice = input("Enter c to create new students, m to manage students and their mark sheets, s for settings and l to logout:")
                menu_item = self.admin_main_menu_dictionary.get(choice)
            if menu_item is None:
                print("Please enter valid choice")
                continue
            menu_item.execute()
            exit_initiated = menu_item.exit_initiated()

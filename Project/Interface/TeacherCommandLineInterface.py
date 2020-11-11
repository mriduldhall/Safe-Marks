from HelperLibrary.Validator import Validator
from Student import Student
from Teacher.Create import Create


class LogoutMenuItem:
    def __init__(self):
        self.is_exit_initiated = False

    def execute(self):
        print("Logging out...")
        self.is_exit_initiated = True

    def exit_initiated(self):
        return self.is_exit_initiated


class SettingsMenuItem:
    def __init__(self):
        pass

    def execute(self):
        pass

    @staticmethod
    def exit_initiated():
        return False


class ManageMenuItem:
    def __init__(self):
        pass

    def execute(self):
        pass

    @staticmethod
    def exit_initiated():
        return False


class CreateMenuItem:
    def __init__(self):
        pass

    def execute(self):
        if Validator("create").should_continue():
            continuation = True
            while continuation is True:
                student = self.getstudentdetails()
                message = Create().create(student)
                print(message)
                continuation = bool(int(input("Enter 1 to create another student and 0 to head back to main menu.")))

    @staticmethod
    def exit_initiated():
        return False

    @staticmethod
    def getstudentdetails():
        name = input("Enter student's name:").capitalize()
        age = input("Enter student's age:")
        year_group = input("Enter student's year group:")
        student = Student(name, age, year_group, teacher="admin")
        return student


class CLI:
    def __init__(self, name):
        self.name = name
        self.mainmenudictionary = {
            "c": CreateMenuItem(),
            "m": ManageMenuItem(),
            "s": SettingsMenuItem(),
            "l": LogoutMenuItem()
        }

    def initiate(self):
        exit_initiated = False
        while not exit_initiated:
            choice = input("Enter c to create new students, m to manage students and their mark sheets, s for settings and l to logout")
            menu_item = self.mainmenudictionary.get(choice)
            if menu_item is None:
                print("Please enter valid choice")
                continue
            menu_item.execute()
            exit_initiated = menu_item.exit_initiated()


if __name__ == '__main__':
    interface = CLI("admin")
    interface.initiate()

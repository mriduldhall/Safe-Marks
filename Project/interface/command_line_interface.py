from enum import Enum

from project.login import Login
from project.registration import Registration
from project.user import User


class AllowedValuesReconformation(Enum):
    stop = "0"
    resume = "1"


class Validator:
    def __init__(self, input_name):
        self.type = input_name

    def validate_separator(self, string):
        if "§" in string:
            print("The", self.type, "is not accepted as it contains '§' which is not accepted.\nPlease try again.")
            return 1
        else:
            return 0

    def should_continue(self):
        while True:
            try:
                print("You have entered the", self.type, "section.")
                decision = AllowedValuesReconformation(
                    input("Do you want to continue?\nEnter 1 to continue or 0 to leave."))
            except ValueError:
                print("Enter valid choice (0, 1)")
            else:
                return decision.value


class ExitMenuItem:

    def __init__(self):
        self.is_exit_initiated = False

    def execute(self):
        print("Exiting...")
        return self.is_exit_initiated

    def exit_initiated(self):
        return self.is_exit_initiated

    def name(self):
        return "Exit program (e)"


class RegisterMenuItem:

    def __init__(self):
        pass

    def name(self):
        return "Register User (r)"

    def exit_initiated(self):
        return False

    def execute(self):
        if Validator("register").should_continue():
            user = self._get_new_user_details()
            msg = Registration("/Users/priyank/Downloads/Safe-Marks/User.txt").register(user)
            print(msg)

        return False

    def _get_new_user_details(self):
        username = input("Please enter your username:")
        username_validator = Validator("username")
        password = input("Please enter a password for you account:")
        password_validator = Validator("password")
        while username_validator.validate_separator(username) or password_validator.validate_separator(password) == 1:
            username = input("Please enter your username:")
            username_validator = Validator("username")
            password = input("Please enter a password for your account:")
            password_validator = Validator("password")
        return User(username, password)


class LoginMenuItem:

    def __init__(self, login_module=Login()):
        self.login_module = login_module
        pass

    def name(self):
        return "Login user (l)"

    def exit_initiated(self):
        return False

    def execute(self):
        if Validator("login").should_continue():
            logged_in = False
            try_again = True
            logged_in_username = None
            while (logged_in is False) and (try_again is True):
                username = input("Enter your username:")
                password = input("Enter your password:")

                login_result = self.login_module.validate_credentials(User(username, password))

                if login_result == Login.logged_in:
                    print("Successfully logged in")
                    logged_in = True
                    try_again = False
                    logged_in_username = username
                elif login_result == Login.does_not_exist:
                    print("Entered username does not exist")
                    try_again = bool(int(input("Would you like to try again? Enter 1 to try again and 0 to exit.")))
                else:
                    print("Incorrect username and/or password")
                    try_again = bool(int(input("Would you like to try again? Enter 1 to try again and 0 to exit.")))

            if logged_in_username is not None:
                teacher_mainmenu(logged_in_username)


class InformationMenuItem:

    def __init__(self):
        pass

    def execute(self):
        print("Currently no information available")
        return False

    def name(self):
        return "Information (i)"

    def exit_initiated(self):
        return False


class CLI:

    def __init__(self):
        self.mainmenu_dict = {
            'r': RegisterMenuItem(),
            'l': LoginMenuItem(),
            'i': InformationMenuItem(),
            'e': ExitMenuItem()
        }

    def initiate(self):
        exit_initiated = False

        while not exit_initiated:
            choice = input(
                "Enter r to register a teacher account, l to login or i to get more information.\nEnter e to exit the software.")
            menu_item = self.mainmenu_dict.get(choice)
            if menu_item is None:
                print("Enter valid choice (l,r, i, e)")
                continue

            menu_item.execute()
            exit_initiated = menu_item.exit_initiated()

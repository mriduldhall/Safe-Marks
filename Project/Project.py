from enum import Enum
from StorageFunctions import StorageFunctions
from Teacher import mainmenu as teacher_mainmenu


class AllowedValuesMainMenu(Enum):
    register = 'r'
    login_not_complete = "l"
    information = "i"
    exit = "e"


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

    def validate_continuation(self):
        while True:
            try:
                print("You have entered the", self.type, "section.")
                decision = AllowedValuesReconformation(
                    input("Do you want to continue?\nEnter 1 to continue or 0 to leave."))
            except ValueError:
                print("Enter valid choice (0, 1)")
            else:
                return decision.value


class User:
    def __init__(self, name, pword):
        self.username = name
        self.password = pword

    def register(self):
        new_user_data = StorageFunctions("/Users/nitindhall/PycharmProjects/Programs/Project/Text Files/User.txt", self.username)
        data, location = new_user_data.retrieve(1)
        if data is None:
            new_user_storage = StorageFunctions("/Users/nitindhall/PycharmProjects/Programs/Project/Text Files/User.txt", self.username + "§" + self.password + "§\n")
            new_user_storage.append()
            print("You have successfully created an account with the username", self.username)
        else:
            print("Username is already taken")

    def login(self):
        logged_in = False
        try_again = True
        while (logged_in is False) and (try_again is True):
            self.username = input("Enter your username:")
            self.password = input("Enter your password:")
            current_user_data = StorageFunctions("/Users/nitindhall/PycharmProjects/Programs/Project/Text Files/User.txt", self.username)
            data, location = current_user_data.retrieve(1)
            if data is None:
                print("Entered username does not exist")
                try_again = bool(int(input("Would you like to try again? Enter 1 to try again and 0 to exit.")))
            else:
                data = data.split("§")
                password_check = data[1]
                if self.password == password_check:
                    print("Successfully logged in")
                    logged_in = True
                    try_again = False
                    logged_in_username = self.username
                else:
                    print("Incorrect username and/or password")
                    try_again = bool(int(input("Would you like to try again? Enter 1 to try again and 0 to exit.")))
        if logged_in_username is not None:
            return logged_in_username
        else:
            return None


def mainmenu():
    while True:
        try:
            main_menu_choice = AllowedValuesMainMenu(input(
                "Enter r to register a teacher account, l to login or i to get more information.\nEnter e to exit the software."))
        except ValueError:
            print("Enter valid choice (l,r, i, e)")
        else:
            return main_menu_choice.value


def getnewuserdetails():
    # TODO Password not visible
    username = input("Please enter your username:")
    username_validator = Validator("username")
    password = input("Please enter a password for you account:")
    password_validator = Validator("password")
    while username_validator.validate_separator(username) or password_validator.validate_separator(password) == 1:
        username = input("Please enter your username:")
        username_validator = Validator("username")
        password = input("Please enter a password for your account:")
        password_validator = Validator("password")
    return username, password


def register():
    register_continuation_validation = Validator("register")
    continuation = bool(int(register_continuation_validation.validate_continuation()))
    if continuation is True:
        username, password = getnewuserdetails()
        new_user = User(username, password)
        new_user.register()
    return False


def login():
    login_continuation_validation = Validator("login")
    continuation = bool(int(login_continuation_validation.validate_continuation()))
    if continuation is True:
        existing_user = User("", "")
        username = existing_user.login()
        if username is not None:
            teacher_mainmenu(username)
    return False


def information():
    print("Currently no information available")
    return False


def exit_software():
    print("Exiting...")
    return True


mainmenu_dict = {'r': register, 'l': login, 'i': information, 'e': exit_software}
if __name__ == "__main__":
    print("Welcome to SafeMarks")
    exit = False
    while exit is False:
        mainmenu_decision = mainmenu()
        exit = mainmenu_dict[mainmenu_decision]()

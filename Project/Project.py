from enum import Enum
from StorageFunctions import StorageFunctions


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
        NewUserData = StorageFunctions("User.txt", self.username)
        Data = NewUserData.retrieve(1)
        if Data is None:
            NewUserStorage = StorageFunctions("User.txt", self.username + "§" + self.password + "§\n")
            NewUserStorage.append()
            print("You have successfully created an account with the username", self.username)
        else:
            print("Username is already taken")

    def login(self):
        while True:
            CurrentUserData = StorageFunctions("User.txt", self.username)
            Data = CurrentUserData.retrieve(1)
            if Data is None:
                print("Entered username does not exist")
                return bool(int(input("Would you like to try again? Enter 1 to try again and 0 to exit.")))
            else:
                Data = Data.split("§")
                password_check = Data[1]
                if self.password == password_check:
                    print("Successfully logged in")
                    return False
                else:
                    print("Incorrect username and/or password")
                    return bool(int(input("Would you like to try again? Enter 1 to try again and 0 to exit.")))


def mainmenu():
    while True:
        try:
            MainMenuChoice = AllowedValuesMainMenu(input(
                "Enter r to register a teacher account, l to login or i to get more information.\nEnter e to exit the software."))
        except ValueError:
            print("Enter valid choice (l,r, i, e)")
        else:
            return MainMenuChoice.value


def getnewuserdetails():
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


def endprogram():
    pass


def userlogin():
    pass


def decision_to_register():
    register_continuation_validation = Validator("register")
    return register_continuation_validation.validate_continuation()


def decision_to_login():
    login_continuation_validation = Validator("login")
    return login_continuation_validation.validate_continuation()


def information():
    pass


def exit_software():
    pass


mainmenu_dict = {'r': decision_to_register, 'l': decision_to_login, 'i': information, 'e': exit_software}
registermenu_dict = {'0': endprogram, '1': getnewuserdetails}
loginmenu_dict = {'0': endprogram, '1': userlogin}
if __name__ == "__main__":
    print("Welcome to SafeMarks")
    correct = 1
    while correct == 1:
        mainmenu_decision = mainmenu()
        continue_decision = mainmenu_dict[mainmenu_decision]()
        if mainmenu_decision == "r":
            username, password = registermenu_dict[continue_decision]()
            NewUser = User(username, password)
            NewUser.register()
        elif mainmenu_decision == "l":
            loginmenu_dict[continue_decision]()
            login_not_complete = True
            while login_not_complete:
                username = input("Please enter your username:")
                password = input("Please enter your password:")
                CurrentUser = User(username, password)
                login_not_complete = CurrentUser.login()

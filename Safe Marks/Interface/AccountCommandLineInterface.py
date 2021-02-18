from HelperLibrary.Validator import Validator
from HelperLibrary.StorageFunctions import StorageFunctions


class ExitMenuItem:
    def __init__(self):
        self.is_exit_initiated = False

    def execute(self):
        print("Exiting...")
        self.is_exit_initiated = True

    def exit_initiated(self):
        return self.is_exit_initiated


class DisableMenuItem:
    def __init__(self):
        pass

    def execute(self):
        pass

    @staticmethod
    def exit_initiated():
        return False


class EnableMenuItem:
    def __init__(self):
        pass

    def execute(self):
        if Validator("enable").should_continue():
            disabled_users_names = self.get_disabled_users_names()
            choice_list_disabled_users_names = bool(int(input("Enter 1 to get a list of all disabled users and 0 to continue without a list of names:")))
            if choice_list_disabled_users_names:
                self.print_disabled_users_names(disabled_users_names)
            user_name = input("Enter disabled user's name to enable:").capitalize()
            if user_name in disabled_users_names:
                self.enable_user(user_name)
                print("Successfully enabled user")
            else:
                print("User does not exist or is not disabled!")

    @staticmethod
    def get_disabled_users_names():
        disabled_users_data = StorageFunctions("users").retrieve(['enabled'], [False])
        disabled_users_names = []
        for disabled_user_data in disabled_users_data:
            disabled_users_names.append(disabled_user_data[1])
        return disabled_users_names

    @staticmethod
    def print_disabled_users_names(disabled_users_names):
        print("Disabled users:")
        counter = 1
        for disabled_user_name in disabled_users_names:
            print(counter, ":", disabled_user_name)
            counter += 1

    @staticmethod
    def enable_user(user_name):
        user_id = StorageFunctions("users").retrieve(['username'], [user_name])[0][0]
        StorageFunctions("users").update(['enabled'], [True], user_id)

    @staticmethod
    def exit_initiated():
        return False


class CLI:
    def __init__(self):
        self.main_menu_dictionary = {
            "1": EnableMenuItem(),
            "2": DisableMenuItem(),
            "3": ExitMenuItem(),
        }

    def initiate(self):
        exit_initiated = False
        while not exit_initiated:
            main_menu_choice = input("Enter 1 to enable accounts, 2 to disable accounts and 3 to exit this menu:")
            menu_item = self.main_menu_dictionary.get(main_menu_choice)
            if menu_item is None:
                print("Please enter a valid choice")
                continue
            menu_item.execute()
            exit_initiated = menu_item.exit_initiated()

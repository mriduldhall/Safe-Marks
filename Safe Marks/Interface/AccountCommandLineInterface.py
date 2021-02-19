from User.Access import ManageAccess


class ExitMenuItem:
    def __init__(self):
        self.is_exit_initiated = False

    def execute(self):
        print("Exiting...")
        self.is_exit_initiated = True

    def exit_initiated(self):
        return self.is_exit_initiated


class DisableMenuItem:
    def __init__(self, singleton):
        self.logged_in_user = singleton.name

    def execute(self):
        message = ManageAccess("disable", self.logged_in_user).execute()
        print(message)

    @staticmethod
    def exit_initiated():
        return False


class EnableMenuItem:
    def __init__(self, singleton):
        self.logged_in_user = singleton.name

    def execute(self):
        message = ManageAccess("enable", self.logged_in_user).execute()
        print(message)

    @staticmethod
    def exit_initiated():
        return False


class CLI:
    def __init__(self, singleton):
        self.main_menu_dictionary = {
            "1": EnableMenuItem(singleton),
            "2": DisableMenuItem(singleton),
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

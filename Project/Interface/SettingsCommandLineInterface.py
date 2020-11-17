from HelperLibrary.Singleton import Singleton
from Settings.EditPassword import EditPassword
from Settings.DeleteAccount import Delete


class ExitMenuItem:
    def __init__(self):
        self.is_exit_initiated = False

    def execute(self):
        print("Exiting...")
        self.is_exit_initiated = True

    def exit_initiated(self):
        return self.is_exit_initiated


class DeleteMenuItem:
    def __init__(self, singleton):
        self.singleton = singleton
        self.is_exit_initiated = False

    def execute(self):
        confirm_continuation = bool(int(input("Enter 1 to change your password and 0 to exit:")))
        if confirm_continuation:
            try_again = True
            while try_again:
                print("Your username is:", self.singleton.getinstance())
                password = input("Enter your password to confirm deletion:")
                message, result = Delete(self.singleton).delete(password)
                print(message)
                if result == Delete.failed:
                    try_again = bool(int(input("Enter 1 to try again and 0 to exit:")))
                else:
                    try_again = False
                    self.is_exit_initiated = True

    def exit_initiated(self):
        return self.is_exit_initiated


class EditPasswordMenuItem:
    def __init__(self, singleton):
        self.singleton = singleton

    def execute(self):
        confirm_continuation = bool(int(input("Enter 1 to change your password and 0 to exit:")))
        if confirm_continuation is True:
            try_again = True
            while try_again:
                print("Your username is:", self.singleton.getinstance())
                confirm_password = input("Enter your old password:")
                new_password = input("Enter your new password:")
                confirm_new_password = input("Confirm password:")
                message, result = EditPassword(self.singleton).editpassword(confirm_password, new_password, confirm_new_password)
                print(message)
                if result == EditPassword.failed:
                    try_again = bool(int(input("Enter 1 to try again and 0 to exit:")))
                else:
                    try_again = False

    @staticmethod
    def exit_initiated():
        return False


class CLI:
    def __init__(self, singleton):
        self.settingsmenu_dict = {
            '1': EditPasswordMenuItem(singleton),
            '2': DeleteMenuItem(singleton),
            '0': ExitMenuItem()
        }

    def initiate(self):
        exit_initiated = False
        while not exit_initiated:
            choice = input("Enter 1 to edit password, 2 to delete account and 0 to exit settings:")
            menu_item = self.settingsmenu_dict.get(choice)
            if menu_item is None:
                print("Please enter valid choice")
                continue
            menu_item.execute()
            exit_initiated = menu_item.exit_initiated()
        if menu_item == self.settingsmenu_dict.get("2"):
            return True
        else:
            return None


if __name__ == '__main__':
    CLI(Singleton("admin")).initiate()

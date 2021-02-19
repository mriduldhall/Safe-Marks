from HelperLibrary.Validator import Validator
from HelperLibrary.StorageFunctions import StorageFunctions


class ManageAccessController:
    def __init__(self, action, table_name):
        self.action = action
        self.table_name = table_name

    def get_user_names(self):
        if self.action == "enable":
            users_data = StorageFunctions(self.table_name).retrieve(['enabled'], [False])
        else:
            users_data = StorageFunctions(self.table_name).retrieve(['enabled'], [True])
        users_names = []
        for user_data in users_data:
            users_names.append(user_data[1])
        return users_names

    def print_users_names(self, users_names):
        if self.action == "enable":
            print("Disabled users:")
        else:
            print("Enabled users:")
        counter = 1
        for user_name in users_names:
            print(counter, ":", user_name)
            counter += 1

    def change_access(self, username):
        user_id = StorageFunctions("users").retrieve(['username'], [username])[0][0]
        if self.action == "enable":
            StorageFunctions(self.table_name).update(['enabled'], [True], user_id)
        else:
            StorageFunctions(self.table_name).update(['enabled'], [False], user_id)


class ManageAccess:
    def __init__(self, action, logged_in_user, table_name="users"):
        assert (action == "enable") or (action == "disable"), "Action is neither enable nor disable"
        self.action = action
        self.logged_in_user = logged_in_user
        self.manage_access_controller = ManageAccessController(action, table_name)

    def execute(self):
        if Validator("enable").should_continue():
            users_names = self.manage_access_controller.get_user_names()
            if self.action == "enable":
                choice_list_users_names = bool(int(input("Enter 1 to get a list of all disabled users and 0 to continue without a list of names:")))
            else:
                choice_list_users_names = bool(int(input("Enter 1 to get a list of all enabled users and 0 to continue without a list of names:")))
            if choice_list_users_names:
                self.manage_access_controller.print_users_names(users_names)
            if self.action == "enable":
                user_name = input("Enter disabled user's name to enable:").capitalize()
            else:
                user_name = input("Enter enabled user's name to disable:").capitalize()
            if user_name == self.logged_in_user:
                return "You cannot " + self.action + " yourself"
            elif user_name in users_names:
                self.manage_access_controller.change_access(user_name)
                return "Successfully " + self.action + "d user"
            else:
                return "User does not exist or is not " + self.action + "d!"

from HelperLibrary.StorageFunctions import StorageFunctions
from User.User import User


class LoginStore:

    def __init__(self, file_path):
        self.storage_file = file_path

    def get_password_by_username(self, username):
        user_data_file = StorageFunctions(self.storage_file, username)
        data, location = user_data_file.retrieve(1)

        if data is None:
            return None

        data = data.split("§")

        if data[0] == username:
            return User(data[0], data[1])
        else:
            return None


class Login:
    logged_in = 1
    does_not_exist = 2
    incorrect_credentials = 3

    def __init__(self, login_store_file_path="/Users/nitindhall/PycharmProjects/Programs/Project/Text Files/User.txt"):
        self.login_store = LoginStore(login_store_file_path)

    def validate_credentials(self, user):
        stored_user = self.login_store.get_password_by_username(user.username)

        if stored_user is None:
            return self.does_not_exist

        if stored_user.password == user.password:
            return self.logged_in
        else:
            return self.incorrect_credentials

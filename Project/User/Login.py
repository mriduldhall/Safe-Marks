from HelperLibrary.StorageFunctionsDatabase import StorageFunctions
from User.User import User


class LoginStore:

    def __init__(self, table_name):
        self.table_name = table_name

    def get_password_by_username(self, username):
        user_data = StorageFunctions(self.table_name).retrieve(["username"], [username])
        if not user_data:
            return None
        elif (user_data[0])[1] == username:
            return User((user_data[0])[1], (user_data[0])[2])
        else:
            return False


class Login:
    logged_in = 1
    does_not_exist = 2
    incorrect_credentials = 3

    def __init__(self, users_table_name="users"):
        self.login_store = LoginStore(users_table_name)

    def validate_credentials(self, user):
        stored_user = self.login_store.get_password_by_username(user.username)
        if stored_user is None:
            return self.does_not_exist
        elif stored_user.password == user.password:
            return self.logged_in
        else:
            return self.incorrect_credentials

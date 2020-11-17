from HelperLibrary.StorageFunctions import StorageFunctions


class RegistrationStore:

    def __init__(self, file_path):
        self.storage_file = file_path

    def user_does_not_exist(self, username):
        sf = StorageFunctions(self.storage_file, username)
        data, location = sf.retrieve(1)
        return data is None

    def add_user(self, user):
        sf = StorageFunctions(self.storage_file, user.username + "§" + user.password + "§\n")
        sf.append()


class Registration:

    def __init__(self, user_storage_path="/Users/nitindhall/PycharmProjects/Programs/Project/Text Files/User.txt"):
        self.user_storage = RegistrationStore(user_storage_path)

    def register(self, user):
        if self.user_storage.user_does_not_exist(user.username):
            self.user_storage.add_user(user)
            return "You have successfully created an account with the username" + user.username
        else:
            return "Username is already taken"

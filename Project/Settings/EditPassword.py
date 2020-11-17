from HelperLibrary.StorageFunctions import StorageFunctions


class EditPasswordStore:
    def __init__(self, user_data_storage_path, username):
        self.user_file = user_data_storage_path
        self.username = username

    def confirmpassword(self, confirm_password):
        data, location = StorageFunctions(self.user_file, confirm_password).retrieve(2)
        if data is not None:
            return True, location
        else:
            return False, location

    def changepassword(self, password, location):
        StorageFunctions(self.user_file, self.username + "§" + password + "§\n").update(location)


class EditPassword:
    successful = 1
    failed = 2

    def __init__(self, singleton,  user_data_storage_path="/Users/nitindhall/PycharmProjects/Programs/Project/Text Files/User.txt"):
        self.edit_password_module = EditPasswordStore(user_data_storage_path, singleton.name)

    def editpassword(self, confirm_password, new_password, confirm_new_password):
        result, location = self.edit_password_module.confirmpassword(confirm_password)
        if result:
            if new_password == confirm_new_password:
                self.edit_password_module.changepassword(new_password, location)
                message = "Password successfully changed"
                return message, self.successful
            else:
                message = "Incorrect re=entered password"
                return message, self.failed
        else:
            message = "Password is incorrect!"
            return message, self.failed

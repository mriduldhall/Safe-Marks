from HelperLibrary.StorageFunctions import StorageFunctions


class EditPasswordStore:
    def __init__(self, user_storage_file_path):
        self.user_file = user_storage_file_path

    def confirmpassword(self, password):
        user_data = StorageFunctions(self.user_file, password)
        data, location = user_data.retrieve(2)
        if data is None:
            return False, str(data), int(location)
        else:
            return True, data, location

    def updatepassword(self, name, password, location):
        user_data = StorageFunctions(self.user_file, name + "§" + password + "§\n")
        user_data.update(location)


class EditPassword:
    def __init__(self, user_storage_file_path):
        self.edit_password_module = EditPasswordStore(user_storage_file_path)

    def editpassword(self, confirm_password, new_password, confirm_new_password):
        exist_check, data, location = self.edit_password_module.confirmpassword(confirm_password)
        if (exist_check is True) and (new_password == confirm_new_password):
            data = str(data)
            data = data.split("§")

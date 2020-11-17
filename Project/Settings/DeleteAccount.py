from HelperLibrary.StorageFunctions import StorageFunctions


class DeleteStore:
    def __init__(self, user_data_storage_path, singleton):
        self.user_file = user_data_storage_path
        self.username = singleton.name

    def confirmpassword(self, password):
        data, location = StorageFunctions(self.user_file, password).retrieve(2)
        if data is not None:
            return True, location
        else:
            return False, location

    def delete_user(self, location):
        StorageFunctions(self.user_file, "").update(location)


class Delete:
    successful = 1
    failed = 2

    def __init__(self, singleton, user_data_storage_path="/Users/nitindhall/PycharmProjects/Programs/Project/Text Files/User.txt"):
        self.delete_module = DeleteStore(user_data_storage_path, singleton)

    def delete(self, password):
        result, location = self.delete_module.confirmpassword(password)
        if result:
            self.delete_module.delete_user(location)
            message = "Account successfully deleted!\nRedirecting to main page..."
            return message, self.successful
        else:
            message = "Password is incorrect!"
            return message, self.failed

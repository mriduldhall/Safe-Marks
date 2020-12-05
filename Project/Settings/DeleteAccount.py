from HelperLibrary.StorageFunctionsDatabase import StorageFunctions as StorageFunctionsDatabase


class DeleteStore:
    def __init__(self, table_name, singleton):
        self.table_name = table_name
        self.username = singleton.name

    def confirmpassword(self, password):
        user_data = StorageFunctionsDatabase(self.table_name).retrieve(["password"], [password])
        if not user_data:
            return False, None
        else:
            return True, (user_data[0])[0]

    def delete_user(self, id):
        StorageFunctionsDatabase(self.table_name).delete(id)


class Delete:
    successful = 1
    failed = 2

    def __init__(self, singleton, users_table_name="users"):
        self.delete_module = DeleteStore(users_table_name, singleton)

    def delete(self, password):
        result, id = self.delete_module.confirmpassword(password)
        if result:
            self.delete_module.delete_user(id)
            message = "Account successfully deleted!\nRedirecting to main page..."
            return message, self.successful
        else:
            message = "Password is incorrect!"
            return message, self.failed

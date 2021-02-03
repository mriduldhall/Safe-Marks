from HelperLibrary.StorageFunctions import StorageFunctions


class EditPasswordStore:
    def __init__(self, table_name, username):
        self.table_name = table_name
        self.username = username

    def confirmpassword(self, password):
        user_data = StorageFunctions(self.table_name).retrieve(["password"], [password])
        if not user_data:
            return False, None
        else:
            return True, (user_data[0])[0]

    def changepassword(self, password, id):
        StorageFunctions(self.table_name).update(["password"], [password], id)


class EditPassword:
    successful = 1
    failed = 2

    def __init__(self, singleton, users_table_name="users"):
        self.edit_password_module = EditPasswordStore(users_table_name, singleton.name)

    def editpassword(self, confirm_password, new_password, confirm_new_password):
        result, id = self.edit_password_module.confirmpassword(confirm_password)
        if result:
            if new_password == confirm_new_password:
                self.edit_password_module.changepassword(new_password, id)
                message = "Password successfully changed"
                return message, self.successful
            else:
                message = "Incorrect re-entered password"
                return message, self.failed
        else:
            message = "Password is incorrect!"
            return message, self.failed

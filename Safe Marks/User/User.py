class User:
    def __init__(self, name, password, admin=False, enabled=False):
        self.username = name
        self.password = password
        self.admin = admin
        self.enabled = enabled

class Singleton:
    __instance = None

    @staticmethod
    def getinstance():
        if Singleton.__instance is None:
            raise Exception("Singleton does not exist!")
        return Singleton.__instance

    def __init__(self, name, admin):
        if Singleton.__instance is not None:
            raise Exception("This class is a singleton!")
        else:
            self.name = name
            self.admin = admin
            Singleton.__instance = True

    @staticmethod
    def reset():
        Singleton.__instance = None

class Singleton:
    __instance = None

    @staticmethod
    def getinstance():
        if Singleton.__instance is None:
            raise Exception("Singleton does not exist!")
        return Singleton.__instance

    def __init__(self, name):
        if Singleton.__instance is not None:
            raise Exception("This class is a singleton!")
        else:
            self.name = name
            Singleton.__instance = self.name

    @staticmethod
    def reset():
        Singleton.__instance = None

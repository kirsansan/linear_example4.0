class ConnectionLostError(Exception):

    def __init__(self, code, message="Error"):
        self.__code = code
        self.__message = message

    @property
    def message(self):
        return self.__message
